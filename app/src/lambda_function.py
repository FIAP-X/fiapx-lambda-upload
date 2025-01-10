import boto3
from botocore.config import Config

def lambda_handler(event, context):

    region_name = os.environ['REGION_NAME']
    access_key_id = os.environ['AWS_ACCESS_KEY_ID']
    secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
    session_token = os.environ.get('AWS_SESSION_TOKEN', None)
    bucket_name = os.environ['BUCKET_NAME']

    s3_client = boto3.client(
        's3',
        region_name = region_name,
        aws_access_key_id = access_key_id,
        aws_secret_access_key = secret_access_key,
        aws_session_token = session_token,
        config = Config(signature_version = "s3v4")
    )

    url = s3_client.generate_presigned_url(
        ClientMethod='put_object',
        Params={'Bucket': bucket_name, 'Key': 'videos/video.mkv',},
        ExpiresIn=60,
    )

    return {"statusCode": 200, "body": url}