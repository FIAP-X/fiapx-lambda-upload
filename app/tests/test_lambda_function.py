import os
from unittest import TestCase, mock
from src.lambda_function import lambda_handler

class TestLambdaHandler(TestCase):

    @mock.patch('lambda_function.boto3.client')
    def test_lambda_handler_success(self, mock_boto3_client):
        os.environ['REGION_NAME'] = 'us-east-1'
        os.environ['LAMBDA_AWS_ACCESS_KEY_ID'] = 'fake_access_key'
        os.environ['LAMBDA_AWS_SECRET_ACCESS_KEY'] = 'fake_secret_key'
        os.environ['BUCKET_NAME'] = 'test-bucket'
        mock_s3_client = mock.Mock()
        mock_boto3_client.return_value = mock_s3_client
        mock_s3_client.generate_presigned_url.return_value = 'http://example.com'
        response = lambda_handler({}, None)
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['body'], 'http://example.com')

    @mock.patch('lambda_function.boto3.client')
    def test_lambda_handler_error(self, mock_boto3_client):
        os.environ['REGION_NAME'] = 'us-east-1'
        os.environ['LAMBDA_AWS_ACCESS_KEY_ID'] = 'fake_access_key'
        os.environ['LAMBDA_AWS_SECRET_ACCESS_KEY'] = 'fake_secret_key'
        os.environ['BUCKET_NAME'] = 'test-bucket'
        mock_boto3_client.side_effect = Exception("Erro simulado ao conectar com o S3")
        response = lambda_handler({}, None)
        self.assertEqual(response['statusCode'], 500)
        self.assertIn("Erro simulado ao conectar com o S3", response['body'])

if __name__ == '__main__':
    unittest.main()