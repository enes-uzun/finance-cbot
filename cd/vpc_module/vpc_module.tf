resource "aws_vpc" "terraform_assesment_vpc" {
  cidr_block = "10.3.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true  
}

resource "aws_subnet" "public_subnet" {
  count = 3
  vpc_id = aws_vpc.terraform_assesment_vpc.id
  cidr_block = element(["10.3.1.0/24", "10.3.2.0/24", "10.3.3.0/24"], count.index)
  availability_zone = "eu-west-2a"
  map_public_ip_on_launch = true
}

resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.terraform_assesment_vpc.id
}
resource "aws_route_table" "rtb_public" {
  vpc_id = aws_vpc.terraform_assesment_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.igw.id
  }
}

resource "aws_route_table_association" "rta_subnet_public" {
  depends_on = [ aws_subnet.public_subnet ]
  count = length(aws_subnet.public_subnet)

  subnet_id      = aws_subnet.public_subnet[count.index].id
  route_table_id = aws_route_table.rtb_public.id
}

output "public_subnet_ids" {
  value = aws_subnet.public_subnet.*.id
}


output "vpc_id" {
  value = aws_vpc.terraform_assesment_vpc.id
}
