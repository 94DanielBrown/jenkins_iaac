# AWS region
region = "us-east-1"
# AWS profile
profile = "personal"

# vars for VPC
# IP CIDR range for vpc used to contain jenkins
vpc_cidr = "10.0.0.0/16"
# IP CIDR range for subnet used to contain jenkins
subnet_cidr = "10.0.1.0/24"
# Availability zone to launch subnet in
availability_zone = "us-east-1a"

# vars for Security
# IP range that can access server through ICMP, SSH and HTTP over port 8080
allowed_ips = "0.0.0.0/0"

# vars for compute
# AMI used to launch instance with that is used to host jenkins
ami_id = "ami-07ebfd5b3428b6f4d"
# Instance type used for server
instance_type = "t2.medium"
