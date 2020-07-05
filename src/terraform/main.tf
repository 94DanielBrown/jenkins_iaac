provider "aws" {
  region                  = var.region
  shared_credentials_file = "~/.aws/credentials"
  profile                 = var.profile
}

module "vpc" {
  source      = "./vpc"
  vpc_cidr    = var.vpc_cidr
  subnet_cidr = var.subnet_cidr
}

module "security_group" {
  source      = "./security_group"
  vpc_id      = module.vpc.vpc_id_out
  allowed_ips = var.allowed_ips
}

module "compute" {
  source        = "./compute"
  ami_id        = var.ami_id
  key_name      = var.key_name
  instance_name = var.instance_name
  instance_type = var.instance_type
  sg_id         = module.security_group.sg_id_out
  subnet_id     = var.subnet_id
}

