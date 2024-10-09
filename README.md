# Spotify Data Pipeline with AWS

This project is an automated data pipeline that extracts data from the Spotify API, processes and stores it in Amazon RDS, and visualizes it using Amazon QuickSight. The pipeline is orchestrated using AWS services, with a weekly trigger to keep the data up-to-date.

## Architecture Overview

The pipeline follows these key stages:

1. **Data Extraction**:
   - **Amazon CloudWatch**: Triggers the pipeline weekly.
   - **AWS Lambda (Data Extractor)**: Uses a Python script to pull data from the Spotify API. Data is extracted in raw form and uploaded to Amazon S3.

2. **Data Storage**:
   - **Amazon S3**: Raw data from Spotify is stored in S3 buckets for further processing.

3. **Data Transformation**:
   - **AWS Lambda (Data Transformer)**: Processes and transforms the raw data from S3 into a format suitable for analysis. This data is then pushed to Amazon RDS.

4. **Data Storage**:
   - **Amazon RDS**: Transformed data is stored in Amazon RDS for easy querying and further analysis.

5. **Data Visualization**:
   - **Amazon QuickSight**: Connects to Amazon RDS to create interactive dashboards and visualizations based on the Spotify data.

## Technologies Used

- **Spotify API**: For data extraction
- **AWS Lambda**: Serverless functions for data extraction and transformation
- **Amazon CloudWatch**: For automated weekly triggers
- **Amazon S3**: Storage for raw data
- **Amazon RDS**: Relational database service to store transformed data
- **Amazon QuickSight**: Visualization tool to create dashboards
- **Python**: For scripting and data manipulation within AWS Lambda functions

## Setup and Deployment

To set up and deploy this pipeline, follow these steps:

1. **AWS Account Setup**:
   - Ensure that you have an AWS account with access to Amazon Lambda, CloudWatch, S3, RDS, and QuickSight.

2. **Create an S3 Bucket**:
   - Set up an S3 bucket where raw data from the Spotify API will be stored.

3. **Set Up AWS Lambda Functions**:
   - **Data Extractor**: Create a Lambda function with the necessary Python script to pull data from Spotify and store it in the S3 bucket.
   - **Data Transformer**: Create a Lambda function to transform data from S3 and store it in RDS.

4. **Set Up Amazon RDS**:
   - Configure an RDS instance for storing transformed data.
   - Set up the necessary database and tables for the transformed data.

5. **Configure Amazon CloudWatch**:
   - Set a CloudWatch rule to trigger the Data Extractor Lambda function weekly.

6. **Set Up Amazon QuickSight**:
   - Connect QuickSight to your RDS instance to build dashboards and visualize data.

## Running the Pipeline

1. The pipeline will automatically trigger each week via CloudWatch.
2. Data is extracted from the Spotify API by the Data Extractor Lambda function and stored in S3.
3. The Data Transformer Lambda function processes data from S3 and pushes it to Amazon RDS.
4. Data in Amazon RDS is available for visualization in Amazon QuickSight.

## Future Improvements

- **Real-time Data Processing**: Integrate streaming data capabilities for real-time data processing.
- **Data Quality Checks**: Implement validation steps to ensure data quality at each stage.
- **Automated Reports**: Set up QuickSight to automatically generate reports and send notifications.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
