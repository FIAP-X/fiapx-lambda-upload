import os
import json
import unittest
from unittest.mock import patch, MagicMock
import uuid
from lambda_function import lambda_handler

class TestLambdaHandler(unittest.TestCase):

    @patch('lambda_function.boto3.client')
    @patch('lambda_function.uuid.uuid4', return_value=uuid.UUID('12345678-1234-5678-1234-567812345678'))
    def test_lambda_handler_success(self, mock_uuid, mock_boto_client):
        os.environ['REGION_NAME'] = 'us-east-1'
        os.environ['LAMBDA_AWS_ACCESS_KEY_ID'] = 'fake-access-key'
        os.environ['LAMBDA_AWS_SECRET_ACCESS_KEY'] = 'fake-secret-key'
        os.environ['BUCKET_NAME'] = 'fake-bucket-name'

        mock_s3_client = MagicMock()
        mock_boto_client.return_value = mock_s3_client
        mock_s3_client.generate_presigned_url.return_value = "https://fakeurl.com"

        event = {
            'requestContext': {
                'authorizer': {
                    'claims': {
                        'sub': 'user123'
                    }
                }
            }
        }
        context = MagicMock()

        response = lambda_handler(event, context)

        self.assertEqual(response['statusCode'], 200)
        self.assertIn("url", json.loads(response['body']))
        self.assertEqual(json.loads(response['body'])['url'], "https://fakeurl.com")
        mock_s3_client.generate_presigned_url.assert_called_once_with(
            ClientMethod='put_object',
            Params={'Bucket': 'fake-bucket-name', 'Key': 'videos/user123/12345678-1234-5678-1234-567812345678'},
            ExpiresIn=3600
        )

    @patch('lambda_function.boto3.client')
    def test_lambda_handler_error(self, mock_boto_client):

        os.environ['REGION_NAME'] = 'us-east-1'
        os.environ['LAMBDA_AWS_ACCESS_KEY_ID'] = 'fake-access-key'
        os.environ['LAMBDA_AWS_SECRET_ACCESS_KEY'] = 'fake-secret-key'
        os.environ['BUCKET_NAME'] = 'fake-bucket-name'

        mock_s3_client = MagicMock()
        mock_boto_client.return_value = mock_s3_client
        mock_s3_client.generate_presigned_url.side_effect = Exception("Error generating URL")

        event = {
            'requestContext': {
                'authorizer': {
                    'claims': {
                        'sub': 'user123'
                    }
                }
            }
        }
        context = MagicMock()

        response = lambda_handler(event, context)

        self.assertEqual(response['statusCode'], 500)
        self.assertIn("error", json.loads(response['body']))
        self.assertEqual(json.loads(response['body'])['error'], "Error generating URL")

    @patch('lambda_function.boto3.client')
    def test_lambda_handler_missing_env_variable(self, mock_boto_client):

        os.environ['REGION_NAME'] = 'us-east-1'
        os.environ['LAMBDA_AWS_ACCESS_KEY_ID'] = 'fake-access-key'
        os.environ['LAMBDA_AWS_SECRET_ACCESS_KEY'] = 'fake-secret-key'

        mock_s3_client = MagicMock()
        mock_boto_client.return_value = mock_s3_client

        event = {
            'requestContext': {
                'authorizer': {
                    'claims': {
                        'sub': 'user123'
                    }
                }
            }
        }
        context = MagicMock()

        response = lambda_handler(event, context)

        self.assertEqual(response['statusCode'], 500)
        self.assertIn("error", json.loads(response['body']))
        self.assertIn("BUCKET_NAME", json.loads(response['body'])['error'])

if __name__ == '__main__':
    unittest.main()
