variable "web_server_id" {
  type = string
}
variable "vpc_id" {
  type = string
}
resource "aws_eip" "web_eip" {
  instance = var.web_server_id
  associate_with_private_ip = "10.3.1.12"
  depends_on = [var.vpc_id]
}
