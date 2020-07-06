#!/bin/sh
AWS_PROFILE="personal"
AWS_REGION="us-east-1"
KEY_NAME=$AWS_PROFILE"_"$AWS_REGION
export KEY_NAME=$KEY_NAME
PEM_LOCATION="$HOME/.aws/pem/$KEY_NAME.pem"
DYNAMIC_INVENTORY="$HOME/dynamic_inventory/dynamic_inventory.py"
ANSIBLE_HOST_KEY_CHECKING=False

BASEDIR=$(dirname "$0")
export TFSTATE_FILE="$BASEDIR/src/terraform/terraform.tfstate"

ansible-playbook -i "$DYNAMIC_INVENTORY" ./src/ansible/jenkins_start.yml \
--user "ubuntu" \
--key-file "$PEM_LOCATION" \
