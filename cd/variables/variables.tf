variable "gpt_api_key" {
  type = string
}

resource "aws_ssm_parameter" "gpt_api_key" {
  name  = "gpt_api_key"
  type  = "SecureString"
  value = var.gpt_api_key
}