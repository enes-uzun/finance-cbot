variable "security_group_name" {
  type = string
}
variable "security_group_id" {
  type = string
}

variable "subnet_id" {
  type = string
}

resource "aws_instance" "web_ec2" {
  ami = "ami-0e5f882be1900e43b"
  instance_type = "t2.micro"
  tags = {
    Name = "Web Server"
  }
  iam_instance_profile = "gpt_server_profile"  
  user_data = file("./web_server/script.sh")
  vpc_security_group_ids = [var.security_group_id]
  subnet_id  = var.subnet_id
  private_ip = "10.3.1.12"  
}

# Create an IAM role for EC2 with S3 access
resource "aws_iam_role" "ec2_role" {
  name = "ec2_s3_role"
  
  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Principal" : {
          "Service" : "ec2.amazonaws.com"
        },
        "Action" : "sts:AssumeRole"
      }
    ]
  })
}

# Attach a policy allowing access to S3 to the IAM role
resource "aws_iam_role_policy_attachment" "s3_access" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess"
  role       = aws_iam_role.ec2_role.name
}

resource "aws_iam_instance_profile" "ec2_instance_profile" {
  name = "gpt_server_profile"
  role = aws_iam_role.ec2_role.name
}

data "aws_iam_policy_document" "parameter_store_policy" {
  statement {
    actions = [
      "ssm:GetParameter"
    ]

    resources = [
      "arn:aws:ssm:*:*:parameter/gpt_api_key"
    ]
  }
}

resource "aws_iam_policy" "parameter_store_policy" {
  name        = "ParameterStorePolicy"
  description = "Allows read access to Parameter Store"

  policy = data.aws_iam_policy_document.parameter_store_policy.json
}

resource "aws_iam_role_policy_attachment" "parameter_store_attachment" {
  role       = aws_iam_role.ec2_role.name
  policy_arn = aws_iam_policy.parameter_store_policy.arn
}

output "Web_server_id" {
  value = aws_instance.web_ec2.id
}

