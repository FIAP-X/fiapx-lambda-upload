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

variable "aws_access_key_id" {
  description = "AWS Access Key ID"
  type        = string
  sensitive   = true
}

variable "aws_secret_access_key" {
  description = "AWS Secret Access Key"
  type        = string
  sensitive   = true
}

variable "aws_session_token" {
  description = "AWS Session Token"
  type        = string
  sensitive   = true
}

variable "bucket_name" {
  description = "Nome do bucket S3"
  type        = string
  default     = "fiapx-bucket-upload"
}