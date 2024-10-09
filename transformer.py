import json
import boto3
import psycopg2
from psycopg2 import extensions, sql

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    
    obj = s3.get_object(Bucket='mybucketforspotifyetl', Key='raw_data/spotify_raw_data.json')
    data = json.load(obj['Body'])

    artists = []
    tracks = []

    conn = psycopg2.connect(
        host="database-for-spotify-etl.c30kweeoo13i.eu-west-3.rds.amazonaws.com",
        port=5432,
        user="postgres",
        password="password", 
        database="postgres", 
        sslmode="require"
    )
    conn.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    cursor = conn.cursor()

    def create_database():
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier("database-for-spotify-etl")))
        print("Database created successfully.")

    try:
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'database-for-spotify-etl';")
        exists = cursor.fetchone()
        if not exists:
            create_database()
    except Exception as e:
        print(f"Error checking database: {e}")
    
    cursor.close()
    conn.close()

    conn = psycopg2.connect(
        host="database-for-spotify-etl.c30kweeoo13i.eu-west-3.rds.amazonaws.com",
        port=5432,
        user="postgres",
        password="password", 
        database="database-for-spotify-etl",
        sslmode="require"
    )
    conn.set_isolation_level(extensions.ISOLATION_LEVEL_AUTOCOMMIT)

    cursor = conn.cursor()

    def create_tables():
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS playlists (
                id VARCHAR(100) PRIMARY KEY,
                name VARCHAR(255),
                description TEXT,
                link VARCHAR(255),
                followers INTEGER,
                image VARCHAR(255),
                owner VARCHAR(255)
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS artists (
                id VARCHAR(255) PRIMARY KEY,
                name VARCHAR(255),
                link VARCHAR(255)
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tracks (
                id VARCHAR(255) PRIMARY KEY,
                name VARCHAR(255),
                added_at DATE,
                link VARCHAR(255),
                duration NUMERIC,
                popularity INTEGER,
                album_name VARCHAR(255)
            );
        """)
        conn.commit()

    create_tables()

    def get_playlist_data():
        return {
            "id": data["id"],
            "name": "ABATEERA" if data["name"] == "ABAT\u2211RA" else data["name"],
            "description": data["description"],
            "link": data["external_urls"]["spotify"],
            "followers": data["followers"]["total"],
            "image": data["images"][0]["url"],
            "owner": data["owner"]["display_name"],
        }

    def other_playlist_data():
        for track in data["tracks"]["items"]:
            data_tmp2 = {
                "name": track["track"]["name"],
                "added_at": track["added_at"].split("T")[0],
                "link": track["track"]["external_urls"]["spotify"], 
                "id": track["track"]["id"], 
                "artists": [artist["name"] for artist in track["track"]["artists"]], 
                "duration": round(float(track["track"]["duration_ms"]) / 60000, 2), 
                "popularity": track["track"]["popularity"], 
                "album": {
                    "album_name": track["track"]["album"]["name"],
                    "link": track["track"]["album"]["external_urls"]["spotify"],
                }
            }
            tracks.append(data_tmp2)

            for artist in track["track"]["artists"]:
                data_tmp1 = {
                    "name": artist["name"],
                    "link": artist["external_urls"]["spotify"],
                    "id": artist["id"],
                }
                if data_tmp1 not in artists:
                    artists.append(data_tmp1)

    def insert_playlist(playlist):
        sql = """
        INSERT INTO playlists (id, name, description, link, followers, image, owner)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id) DO NOTHING
        """
        params = (playlist["id"], playlist["name"], playlist["description"], 
                  playlist["link"], playlist["followers"], playlist["image"], 
                  playlist["owner"]) \
                  
        cursor.execute(sql, params)
        conn.commit()

    def insert_artists(artists):
        for artist in artists:
            cursor.execute("""
                INSERT INTO artists (id, name, link)
                VALUES (%s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (artist["id"], artist["name"], artist["link"]))
        conn.commit()

    def insert_tracks(tracks):
        for track in tracks:
            cursor.execute("""
                INSERT INTO tracks (id, name, added_at, link, duration, popularity, album_name)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (track["id"], track["name"], track["added_at"], track["link"], track["duration"], track["popularity"], track["album"]["album_name"]))
        conn.commit()

    playlist = get_playlist_data()
    other_playlist_data()
    
    insert_playlist(playlist)
    insert_artists(artists)
    insert_tracks(tracks)

    cursor.close()
    conn.close()

    return {
        "statusCode": 200,
        "body": "Data processed successfully."
    }
