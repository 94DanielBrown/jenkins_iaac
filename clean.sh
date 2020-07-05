#!/bin/sh
cd src/main/resources/terraform
terraform destroy --auto-approve
rm terraform.{plan,tfstate,tfstate.backup}
