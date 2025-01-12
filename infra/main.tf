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

resource "aws_api_gateway_resource" "lambda_resource" {
  rest_api_id = var.api_gateway_id
  parent_id   = var.api_gateway_root_resource_id
  path_part   = "generate-url"
}

resource "aws_api_gateway_method" "lambda_method" {
  rest_api_id   = var.api_gateway_id
  resource_id   = aws_api_gateway_resource.lambda_resource.id
  http_method   = "POST"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda_integration" {
  rest_api_id             = var.api_gateway_id
  resource_id             = aws_api_gateway_resource.lambda_resource.id
  http_method             = aws_api_gateway_method.lambda_method.http_method
  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = "arn:aws:apigateway:${var.aws_region}:lambda:path/2015-03-31/functions/${aws_lambda_function.lambda_upload.arn}/invocations"
}

resource "aws_lambda_permission" "allow_api_gateway" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_upload.function_name
  principal     = "apigateway.amazonaws.com"
}

resource "aws_api_gateway_deployment" "api_deployment" {
  rest_api_id = var.api_gateway_id
  stage_name  = "prod"
}
