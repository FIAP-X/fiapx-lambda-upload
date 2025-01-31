terraform {
  backend "s3" {
    bucket = "fiapx-statefile-bucket"
    key    = "lambda-upload/terraform.tfstate"
    region = "us-east-1"
  }
}