resource "aws_lambda_function" "lambda_upload" {
  function_name    = var.lambda_function_name
  handler          = var.lambda_handler
  runtime          = var.lambda_runtime
  role             = var.lambda_role
  filename         = var.lambda_zip_path
  source_code_hash = filebase64sha256(var.lambda_zip_path)

  environment {
    variables = {
      REGION_NAME                  = var.aws_region
      LAMBDA_AWS_ACCESS_KEY_ID     = var.lambda_aws_access_key_id
      LAMBDA_AWS_SECRET_ACCESS_KEY = var.lambda_aws_secret_access_key
      BUCKET_NAME                  = var.bucket_name
    }
  }
}