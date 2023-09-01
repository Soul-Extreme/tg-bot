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

  attribute {
      name = "full_name"
      type = "S"
  }

  attribute {
      name = "preferred_name"
      type = "S"
  }

  attribute {
      name = "student_status"
      type = "B"
  }

  attribute {
      name = "nric_last4"
      type = "S"
  }

  attribute {
    name = "cluster"
    type = "S"
  }

  attribute {
    name = "course"
    type = "S"
  }

  attribute {
    name = "year"
    type = "N"
  }

  attribute {
    name = "graduation_year"
    type = "N"
  }

  attribute {
    name = "emergency_contact"
    type = "S"
  }

  attribute {
    name = "emergency_contact_relation"
    type = "S"
  }

  attribute {
    name = "emergency_contact_number"
    type = "S"
  }
}