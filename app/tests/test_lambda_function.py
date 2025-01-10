import unittest
from unittest.mock import patch, MagicMock
from src.lambda_function import lambda_handler


class TestLambdaFunction(unittest.TestCase):

    @patch('boto3.client')
    @patch('os.environ.get')
    def test_generate_presigned_url(self, mock_environ_get, mock_boto3_client):
        mock_environ_get.side_effect = lambda key: {
            'REGION_NAME': 'us-east-1',
            'AWS_ACCESS_KEY_ID': 'mock-access-key-id',
            'AWS_SECRET_ACCESS_KEY': 'mock-secret-access-key',
            'AWS_SESSION_TOKEN': 'mock-session-token',
            'BUCKET_NAME': 'mock-bucket'
        }.get(key)

        mock_s3_client = MagicMock()
        mock_s3_client.generate_presigned_url.return_value = "https://mock-url"
        mock_boto3_client.return_value = mock_s3_client

        event = {}
        context = {}
        response = lambda_handler(event, context)

        mock_boto3_client.assert_called_once_with(
            's3',
            region_name='us-east-1',
            aws_access_key_id='mock-access-key-id',
            aws_secret_access_key='mock-secret-access-key',
            aws_session_token='mock-session-token',
            config=mock_boto3_client().config
        )

        mock_s3_client.generate_presigned_url.assert_called_once_with(
            ClientMethod='put_object',
            Params={'Bucket': 'mock-bucket', 'Key': 'videos/video.mkv'},
            ExpiresIn=60
        )

        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['body'], "https://mock-url")


if __name__ == '__main__':
    unittest.main()
