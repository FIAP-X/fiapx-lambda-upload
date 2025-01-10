import unittest
from unittest.mock import patch, MagicMock
import os
from src.lambda_function import lambda_handler

class TestLambdaFunction(unittest.TestCase):

    def setUp(self):
        
        self.env_vars = {
            'REGION_NAME': 'us-east-1',
            'AWS_ACCESS_KEY_ID': 'test-access-key-id',
            'AWS_SECRET_ACCESS_KEY': 'test-secret-access-key',
            'AWS_SESSION_TOKEN': 'test-session-token',
            'BUCKET_NAME': 'test-bucket-name'
        }
        os.environ.update(self.env_vars)

        self.event = {}
        self.context = {}

    @patch('boto3.client')
    def test_generate_presigned_url(self, mock_boto3_client):
        
        mock_s3_client = MagicMock()
        mock_s3_client.generate_presigned_url.return_value = "https://mock-presigned-url"
        mock_boto3_client.return_value = mock_s3_client

        response = lambda_handler(self.event, self.context)

        mock_boto3_client.assert_called_with(
            's3',
            region_name=self.env_vars['REGION_NAME'],
            aws_access_key_id=self.env_vars['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=self.env_vars['AWS_SECRET_ACCESS_KEY'],
            aws_session_token=self.env_vars['AWS_SESSION_TOKEN'],
            config=mock_boto3_client().config
        )
        
        mock_s3_client.generate_presigned_url.assert_called_once_with(
            ClientMethod='put_object',
            Params={'Bucket': self.env_vars['BUCKET_NAME'], 'Key': 'videos/video.mkv'},
            ExpiresIn=60
        )

        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['body'], "https://mock-presigned-url")

    def test_missing_environment_variables(self):
        
        del os.environ['AWS_ACCESS_KEY_ID']
        with self.assertRaises(KeyError):
            lambda_handler(self.event, self.context)

if __name__ == '__main__':
    unittest.main()