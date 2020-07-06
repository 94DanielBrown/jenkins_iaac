#!/bin/sh
cd src/terraform
terraform destroy --auto-approve -var='key_name=key'
rm terraform.{plan,tfstate,tfstate.backup} &>/dev/null
