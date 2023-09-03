terraform {
  required_version = ">= 1.5.5"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 5.15.0"
    }
  }

  backend "s3" {
    bucket          = module.terraform_state_resources.se_te_bot_terraform_state_s3_bucket_name
    region          = var.aws_region
    key             = "./state/terraform.tfstate"  # Path to where the terraform state file will be stored in the S3
    encrypt         = true
    dynamodb_table  = module.terraform_state_resources.se_tg_bot_terraform_locks_table
  }
}

provider "aws" {
  region = var.aws_region
}