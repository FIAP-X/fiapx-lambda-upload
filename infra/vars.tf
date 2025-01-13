variable "aws_region" {
  description = "Região da AWS"
  type        = string
  default     = "us-east-1"
}

variable "lambda_runtime" {
  description = "Ambiente de execução"
  default     = "python3.12"
}

variable "lambda_role" {
  description = "ARN da role IAM"
  type        = string
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

variable "bucket_upload_name" {
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