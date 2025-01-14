import os
import json
import uuid
import boto3
from botocore.config import Config

def lambda_handler(event, context):
    try:
        region_name = os.environ['REGION_NAME']
        access_key_id = os.environ['LAMBDA_AWS_ACCESS_KEY_ID']
        secret_access_key = os.environ['LAMBDA_AWS_SECRET_ACCESS_KEY']
        session_token = os.environ.get('LAMBDA_AWS_SESSION_TOKEN', None)
        bucket_name = os.environ['BUCKET_NAME']

        s3_client = boto3.client(
            's3',
            region_name=region_name,
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            aws_session_token=session_token,
            config=Config(signature_version="s3v4")
        )

        user_id = event['requestContext']['authorizer']['claims']['sub']

        unique_key = str(uuid.uuid4())

        key = f'videos/{user_id}/{unique_key}'

        url = s3_client.generate_presigned_url(
            ClientMethod = 'put_object',
            Params = {
                'Bucket': bucket_name,
                'Key': key
            },
            ExpiresIn = 3600,
        )

        return {"statusCode": 200, "body": json.dumps({"url": url})}

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}