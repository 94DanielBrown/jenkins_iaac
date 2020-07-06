#!/bin/python3

import os
import re
import json
import argparse

debug = False


class Provider(object):
    """Provider is an abstract class which puts for the interface needed to be implemented
       for the dynamic inventory to be able to use that provider:

        - are_prerequisites_met
            - This checks to make sure that any environment variables or files exist

        - get_all
            - Gets all of the hosts

        - get_host
            - Gets information about a single provided hostname
       """

    def prerequisites_met(args):
        raise NotImplementedError("Should have implemented this")

    def get_all():
        raise NotImplementedError("Should have implemented this")

    def get_host(host):
        raise NotImplementedError("Should have implemented this")


class TestProvider(Provider):

    def prerequisites_met(args):
        debugger("Checking Prerequisites")
        if (args.test):
            return True
        debugger("Prerequisites didn't match")
        return False

    def get_all():
        debugger("Getting all hosts")
        return {
            "test-group": {
                "hosts": ["127.0.0.1", "0.0.0.0"],
                "vars": {
                    "ansible_ssh_user": "admin",
                    "ansible_ssh_private_key_file": "~/.ssh/id_rsa.pub",
                    "is_this_a_test": "yes",
                    "key": "value"
                }
            },
            "_meta": {
                "hostvars": {
                    "127.0.0.1": {
                        "host_specific_var": "bar"
                    },
                    "0.0.0.0": {
                        "host_specific_var": "foo"
                    }
                }
            }
        }

    def get_host(host):
        debugger("Getting details of host: " + str(host))
        if (host == "127.0.0.1"):
            return {"host_specific_var": "bar"}
        if (host == "0.0.0.0"):
            return {"host_specific_var": "foo"}
        return {}


class Terraform(Provider):

    def prerequisites_met(args):
        debugger("Checking Prerequisites")
        if 'TFSTATE_FILE' in os.environ:
            TFSTATE_FILE = os.environ.get('TFSTATE_FILE')
            debugger("Found value for TFSTATE_FILE: " + TFSTATE_FILE)
            if os.path.isfile(TFSTATE_FILE):
                debugger("TFSTATE_FILE exists")
                debugger("Prerequisites match")
                return True

        debugger("Prerequisites didn't match")
        return False

    def get_all():
        debugger("Getting terraform all hosts")
        data = {'_meta': {'hostvars': {}}}
        with open(os.environ.get('TFSTATE_FILE'), 'r') as tfstate_file:
            debugger("File read")
            TFSTATE = json.load(tfstate_file)

        instances = Terraform.get_resource_by_type(TFSTATE, "aws_instance")
        images = Terraform.get_resource_by_type(TFSTATE, "aws_ami")
        eips = Terraform.get_resource_by_type(TFSTATE, "aws_eip")

        for instance in instances:
            group_name = Terraform.get_groupname(instance)
            if group_name == "":
                continue;
            Terraform.swap_eip(instance, eips)
            Terraform.add_to_group(data, group_name, instance)
            Terraform.add_meta(data, instance, images)
        return data

    def swap_eip(instance, eips):
        for eip in eips:
            if(Terraform.get_attribute(instance, 'id') == Terraform.get_attribute(eip, 'instance')):
                instance['attributes']['public_ip'] = Terraform.get_attribute(eip, 'public_ip')
                instance['attributes']['public_dns'] = Terraform.get_attribute(eip, 'public_dns')

    def get_host(hostname):
        debugger("Getting details of host: " + str(hostname))
        with open(os.environ.get('TFSTATE_FILE'), 'r') as tfstate_file:
            debugger("File read")
            TFSTATE = json.load(tfstate_file)

        instances = Terraform.get_resource_by_type(TFSTATE, "aws_instance")
        images = Terraform.get_resource_by_type(TFSTATE, "aws_ami")
        for instance in instances:
            if (hostname == Terraform.get_public_ip(instance)):
                return Terraform.get_hostvars(instance, images)
        return {}

    def add_meta(data, instance, images):
        public_ip = Terraform.get_public_ip(instance)
        if (public_ip not in data['_meta']['hostvars']):
            data['_meta']['hostvars'][public_ip] = {}

        data['_meta']['hostvars'][public_ip] = Terraform.get_hostvars(instance, images)

    def get_hostvars(instance, images):
        raz = Terraform.get_attribute(instance, 'availability_zone')
        region = raz[:-1]
        availability_zone = raz[-1:]
        return {
            'id': Terraform.get_instance_id(instance),
            'private_ip': Terraform.get_private_ip(instance),
            'instance_name': Terraform.get_instance_name(instance),
            'volume_id': Terraform.get_volume_id(instance),
            'availability_zone': availability_zone,
            'region': region,
            'tags': Terraform.get_tags(instance),
            'ami': Terraform.get_image_info(instance, images)
        }

    def add_to_group(data, group, instance):
        if (group not in data):
            data[group] = {'hosts': [], 'vars': {}}
        public_ip = Terraform.get_public_ip(instance)
        data[group]['hosts'].append(public_ip)

    def get_image_info(instance, images):
        data = {}
        data['id'] = Terraform.get_attribute(instance, 'ami')
        debugger("looking for image with id: " + data['id'])
        for image in images:
            image_id = Terraform.get_attribute(image, 'id')
            debugger("checking image with id: " + image_id)
            if (image_id == data['id']):
                data['name']  = Terraform.get_attribute(image, 'name')
                data['owner_id'] = Terraform.get_attribute(image, 'owner_id')
                data['description'] = Terraform.get_attribute(image, 'description')
                data['architecture'] = Terraform.get_attribute(image, 'architecture')
                data['creation_date'] = Terraform.get_attribute(image, 'creation_date')
                data['tags'] = Terraform.get_tags(image)
        return data

    def get_tags(instance):
        # Tech Debt need more tfstates to tell if this is sane
        return instance['attributes']['tags']

    def get_instance_id(instance):
        return Terraform.get_attribute(instance, 'id')

    def get_volume_id(instance):
        return Terraform.get_attribute(instance, 'root_block_device')

    def get_instance_name(instance):
        return Terraform.get_tags(instance)['Name']

    def get_private_ip(instance):
        return Terraform.get_attribute(instance, 'private_ip')

    def get_public_ip(instance):
        return Terraform.get_attribute(instance, 'public_ip')

    def get_attribute(instance, key):
        return instance['attributes'][key]

    def get_resource_by_type(tfstate_file, resource_type):
        all_resources = Terraform.get_resources(tfstate_file)
        resources = [instance for instance in all_resources if instance['type'] == resource_type]
        instances = []
        for resource in resources:
            instances = instances + resource['instances']
        return instances

    def get_resources(tfstate_file):
        return tfstate_file['resources']

    def get_groupname(resource):
        tags = Terraform.get_tags(resource)
        if "Group" in tags:
            return tags["Group"]
        return ""


def read_cli_args():
    global debug
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Used to print debug info about what\'s going on')
    parser.add_argument('--list', action='store_true', help='List the hosts')
    parser.add_argument('--host', action='store', help='Get all hosts')
    parser.add_argument(
        '-f',
        '--file',
        action='store',
        help='Used to pass a file in manually for testing',
        type=str)
    parser.add_argument(
        '--test', action='store_true', help='Use the test provider')
    args = parser.parse_args()

    if (args.debug):
        debug = args.debug
        print("DEBUG MODE: ACTIVE!")
        print("-ARGS-")
        print("list: " + str(args.list))
        print("host: " + str(args.host))
        print("file: " + str(args.file))
        print("test: " + str(args.test))
        print("------")

    return args


def merge_data(data, provider_data):
    if (type(provider_data) is list):
        for item in provider_data:
            if item not in data:
                data.append(item)
    elif (type(provider_data) is str):
        if data == provider_data:
            pass
        else:
            raise Exception("Can't merge data")
    else:
        for key, value in provider_data.items():
            if (key in data):
                if (data[key] == value):
                    pass
                merge_data(data[key], value)
            else:
                data[key] = value


def debugger(message):
    global debug
    if (debug):
        print(message)


def main():
    data = {}
    providers = [TestProvider, Terraform]
    args = read_cli_args()

    for provider in providers:

        provider_data = {}
        debugger("### " + provider.__name__ + " ###")

        if (provider.prerequisites_met(args)):
            if (args.list):
                provider_data = provider.get_all()

            if (args.host):
                provider_data = provider.get_host(args.host)

        debugger(json.dumps(provider_data, indent=4))
        merge_data(data, provider_data)

    debugger("### Full data ###")
    debugger(json.dumps(data, indent=4))
    print(json.dumps(data))


if (__name__ == "__main__"):
    main()
