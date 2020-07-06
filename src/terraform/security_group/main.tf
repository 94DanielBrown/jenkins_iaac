resource "aws_security_group" "main" {
  description = "Allow ssh,icmp and access to jenkins"
  vpc_id      = var.vpc_id

  # ssh 
  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = [var.allowed_ips]
  }
  # icmp
  ingress {
    from_port   = 25
    to_port     = 25
    protocol    = "icmp"
    cidr_blocks = [var.allowed_ips]
  }
  # jenkins
  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = [var.allowed_ips]
  }
  # outbound
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "sg-jenkins"
  }
}
