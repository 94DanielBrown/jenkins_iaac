variable "region" {
  description = "aws region to deploy infrastructure"
}

variable "profile" {
  description = "aws profile to use to deploy infrastructure"
}

#-------- vars for vpc
variable "vpc_cidr" {}
variable "subnet_cidr" {}
variable "availability_zone" {}

#-------- vars for security_group 
variable "allowed_ips" {}

#-------- vars for compute
variable "ami_id" {}
variable "key_name" {}
variable "instance_type" {}
variable "instance_name" {}
variable "subnet_id" {}

