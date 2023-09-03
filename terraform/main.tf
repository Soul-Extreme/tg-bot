module "terraform_state_resources" {
  source = "./modules/terraform_state"
}

module "se_tg_bot_storage" {
  source = "./modules/storage"
}
