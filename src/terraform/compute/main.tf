resource "aws_instance" "main" {
  ami                         = var.ami_id
  instance_type               = var.instance_type
  vpc_security_group_ids      = [var.sg_id]
  key_name                    = var.key_name
  subnet_id                   = var.subnet_id
  associate_public_ip_address = true

  tags = {
    Name  = "jenkins"
    Group = "jenkins"
  }
}

