resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr

  tags = {
    Name = "vpc-jenkins"
  }
}

resource "aws_subnet" "primary" {
  vpc_id                  = aws_vpc.main.id
  cidr_block              = var.subnet_cidr
  map_public_ip_on_launch = true

  tags = {
    Name = "sn-jenkins"
  }
}

resource "aws_internet_gateway" "this" {
  vpc_id = aws_vpc.main.id

  tags = {
    Name = "igw-jenkins"
  }
}

resource "aws_default_route_table" "public" {
  default_route_table_id = aws_vpc.main.main_route_table_id

  tags = {
    Name = "rt-jenkins"
  }
}

resource "aws_route" "public_internet_gateway" {
  route_table_id         = aws_default_route_table.public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.this.id

  timeouts {
    create = "5m"
  }
}

