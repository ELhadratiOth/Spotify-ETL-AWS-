import os
import requests
import json
import boto3


CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

TOKEN_URL = "https://accounts.spotify.com/api/token"
PLAYLIST_URL = "https://api.spotify.com/v1/playlists/{}?offset=0&limit=1"



def get_access_token():
    payload = {
        "grant_type": "client_credentials"
    }
    response = requests.post(TOKEN_URL, data=payload, auth=(CLIENT_ID, CLIENT_SECRET))
    response_data = response.json()

    if response.status_code == 200:
        return response_data["access_token"]
    else:
        print(f"Failed to get access token: {response_data}")
        return None

def get_playlist_tracks(access_token, playlist_id):
    url = PLAYLIST_URL.format(playlist_id)
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch playlist tracks: {response.status_code}, {response.json()}")
        return None

def save_tracks_to_s3(tracks, bucket_name):
    client = boto3.client('s3')
    
    filename = f"spotify_raw_data.json"
    
    try:
        client.put_object(
            Bucket=bucket_name,
            Key=f"raw_data/{filename}",
            Body=json.dumps(tracks)
        )
        print(f"Tracks successfully uploaded to {bucket_name}/raw_data/{filename}")
    except Exception as e:
        print(f"Failed to upload to S3: {e}")

def lambda_handler(event, context):
    access_token = get_access_token()
    print(f"Access Token: {access_token}")

    playlist_id = "37i9dQZF1DWYtEjm4ihp5w"  # ABATEERA playlist id
    if access_token:
        playlist_tracks = get_playlist_tracks(access_token, playlist_id)
        if playlist_tracks:
            save_tracks_to_s3(playlist_tracks, "mybucketforspotifyetl") 
    return {"statusCode": 200, "body": "Success"}
