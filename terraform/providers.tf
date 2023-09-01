terraform {
  required_version = ">= 1.5.5"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      Version = ">= 5.15.0"
    }
  }
}

provider "aws" {
  region = "ap-southeast-1"
}