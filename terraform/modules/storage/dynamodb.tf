# ------------------------------------------------------------
# Personal Particulars
# ------------------------------------------------------------
resource "aws_dynamodb_table" "personal_particulars_table" {
  name          = "personal-particulars"
  billing_mode  = var.dynamodb_billing_mode
  hash_key      = var.chat_id_attribute

  attribute {
    name = var.chat_id_attribute
    type = var.dynamodb_attribute_type_number
  }
}

# ------------------------------------------------------------
# Member Profile
# ------------------------------------------------------------
resource "aws_dynamodb_table" "member_profile_table" {
  name         = "member-profile"
  billing_mode = var.dynamodb_billing_mode
  hash_key     = var.chat_id_attribute

  attribute {
    name = var.chat_id_attribute
    type = var.dynamodb_attribute_type_number
  }
}