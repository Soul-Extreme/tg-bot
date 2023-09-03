output "se_tg_bot_terraform_state_s3_arn" {
  value       = aws_s3_bucket.terraform_state_bucket.arn
  description = "The ARN of the provisioned S3 bucket for storing the terraform state"
}

output "se_tg_bot_terraform_locks_table" {
  value       = aws_dynamodb_table.terraform_locks_table.name
}