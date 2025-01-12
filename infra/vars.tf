variable "aws_region" {
  description = "Região da AWS"
  type        = string
  default     = "us-east-1"
}

variable "lambda_function_name" {
  description = "Nome da função Lambda"
  default     = "fiapx-lambda-upload"
}

variable "lambda_handler" {
  description = "Handler da função Lambda"
  default     = "lambda_function.lambda_handler"
}

variable "lambda_runtime" {
  description = "Ambiente de execução"
  default     = "python3.12"
}

variable "lambda_role" {
  description = "ARN da role IAM"
  default     = "arn:aws:iam::733005211464:role/LabRole"
}

variable "lambda_zip_path" {
  description = "Caminho do arquivo do pacote de implantação"
  default     = "../lambda_function.zip"
}

variable "lambda_aws_access_key_id" {
  description = "AWS Access Key ID"
  type        = string
  sensitive   = true
}

variable "lambda_aws_secret_access_key" {
  description = "AWS Secret Access Key"
  type        = string
  sensitive   = true
}

variable "bucket_name" {
  description = "Nome do bucket S3"
  type        = string
}

variable "api_gateway_id" {
  description = "ID do API Gateway"
  type        = string
}

variable "api_gateway_root_resource_id" {
  description = "ID do recurso raiz da API Gateway"
  type        = string
}

variable "cognito_user_pool_arn" {
  description = "ARN do Cognito User Pool"
  type        = string
}

variable "cognito_user_pool_id" {
  description = "O ID do pool de usuários do Cognito"
  type        = string
}

variable "cognito_app_client_id" {
  description = "O ID do cliente do aplicativo no Cognito"
  type        = string
}