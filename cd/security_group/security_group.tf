variable "vpc_id" {
  type = string
}

resource "aws_security_group" "web_security_group" {
  name = "HTTP HTTPS ALLOW 2"
  vpc_id = var.vpc_id

  dynamic "egress" {
    iterator = port
    for_each = var.egress_port
    content {
      protocol = "TCP"
      from_port = port.value
      to_port = port.value
      cidr_blocks = ["0.0.0.0/0"]
    }
  }
  dynamic "ingress" {
    iterator = port
    for_each = var.ingress_port
    content {
      protocol = "TCP"
      from_port = port.value
      to_port = port.value
      cidr_blocks = ["0.0.0.0/0"]
    }
  }  
}


variable "egress_port" {
  type = list(number)
  default = [80, 443]
}

variable "ingress_port" {
  type = list(number)
  default = [80, 443, 22, 8080, 8000, 8501]
}

output "security_group_name" {
  value = aws_security_group.web_security_group.name
}

output "security_group_id" {
  value = aws_security_group.web_security_group.id
}