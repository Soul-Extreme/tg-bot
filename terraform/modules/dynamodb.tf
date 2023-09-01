# ------------------------------------------------------------
# Personal Particulars
# ------------------------------------------------------------
resource "aws_dynamodb_table" "personal-particulars-table" {
  name          = "personal_particulars"
  billing_mode  = "PAY_PER_REQUEST"
  hash_key      = "chat_id"

  attribute {
    name = "chat_id"
    type = "N"
  }
}