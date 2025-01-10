terraform {
  backend "s3" {
    bucket = "fiapx-bucket-statefile"
    key    = "lambda-upload/terraform.tfstate"
    region = "us-east-1"
  }
}