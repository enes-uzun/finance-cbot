provider "aws" {
  region = "eu-west-2"
}

variable "chat_gpt_api_key" {
  type = string
  description = "CHAT GPT API KEY"
}

module "variables" {
  source = "./variables"
  gpt_api_key = var.chat_gpt_api_key
}

module "web_server" {
  source = "./web_server"
  security_group_name = module.security_group.security_group_name
  subnet_id = module.vpc_module.public_subnet_ids[0]
  security_group_id = module.security_group.security_group_id
}
module "vpc_module" {
  source = "./vpc_module"
}

module "elastic_ip" {
  source = "./elastic_ip"
  web_server_id = module.web_server.Web_server_id
  vpc_id = module.vpc_module.vpc_id
}

module "security_group" {
  source = "./security_group"
  vpc_id = module.vpc_module.vpc_id
}
