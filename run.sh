#!/bin/sh
AWS_PROFILE="personal"
AWS_REGION="us-east-1"
PEM_LOCATION="$HOME/.aws/pem/${AWS_PROFILE}_${AWS_REGION}.pem"
DYNAMIC_INVENTORY="$HOME/dynamic-inventory/dynamic-inventory.py"
ANSIBLE_HOST_KEY_CHECKING=False

BASEDIR=$(dirname "$0")
export TFSTATE_FILE="$BASEDIR/src/terraform/terraform.tfstate"

ansible-playbook -i "$DYNAMIC_INVENTORY" ./src/ansible/jenkins_start.yml \
--user "ubuntu" \
--key-file "$PEM_LOCATION" \
