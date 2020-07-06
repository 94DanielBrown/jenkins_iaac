# jenkins_iaac
IaaC to bring up jenkins on AWS EC2

## Requirements
Ansible  
Terraform  
Python
Unix shell  
AWS private key file

## Usage

Before first use initialise terraform modules with ./init_terraform.sh

## RUN (run.sh)  
Brings up infrastructure in AWS and configures it with ansible so it is a functioning jenkins server. 
### Key location
Private key location from EC2 key pair used to provision server and then connect to it with ansible is set in vars here and should be changed.  
If keys are stored in **$home/.aws/pem/** and use the form **profile_region.pem** then just change the **AWS_PROFILE** and **AWS_REGION** variables
### Users ssh access
A user dbrown is currenly added, remove this user and add others in: **src/ansible/roles/users/defaults/main.yml** with the users public keys in  
**/src/ansible/roles/users/files/username** e.g a file **/src/ansible/roles/users/files/dbrown** contains dbrowns public key
### Terraform vars  
Terraform which may require changing changong such as the allowed ip range for the security group are set in:  
**src/terraform/terraform.tfvars**

 ## RESTORE (restore.sh)
 Restores a jenkins configuration stored in S3  
 Backup variables for locating the backup need to be set in: **src/ansible/vars/backup_vars.yml**  
When the script is ran it will also ask you for aws cli credentials which are used for retrieving the backup from S3

## CLEAN (clean.sh)
 Brings down infrastructure and removes leftover terraform config files  
 Should also be used after a failed deployment attempt
