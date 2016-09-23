#!/usr/bin/env python


import json
import os


class BuildInventory (object):

    def __init__(self):
        self.changed = False
        self.result = ''
        self.heat_upgrade_data = ''
        self.heat_node_data = ''
        self.tripleo_services = {}


    def read_heat_output(self, heat_output_file, var_name):
        if os.path.exists(heat_output_file):
            data = open(heat_output_file).read()
            heat_output_data = json.loads(data)

            if var_name is 'heat_upgrade_data':
                self.heat_upgrade_data = heat_output_data
            if var_name is 'heat_node_data':
                self.heat_node_data = heat_output_data
            return True
        else:
            self.result = ('File %s not found' % heat_output_file)
            self.changed = False
            return False


    def build_inventory_file(self):
        heat_upgrade_data = self.heat_upgrade_data
        heat_node_data = self.heat_node_data

        inventory_file = open('/etc/tripleo/upgrade-inventory', 'w')

        undercloud_role = 'undercloud'
        localhost = 'localhost  ansible_connection=local'
        inventory_file.write('[%s]\n' % undercloud_role)
        inventory_file.write('%s\n' % localhost)

        for role in heat_upgrade_data.keys():
            inventory_file.write('\n[%s]\n' % role)

            for hosts in heat_node_data[role]:
                inventory_file.write('%s\n' % hosts)
            self.write_common_data(inventory_file, role)

            for service in heat_upgrade_data.get(role):
                # Write in the services later so the inventory
                # is more readable
                self.tripleo_services[role] = service

        self.write_service_list(inventory_file)
        inventory_file.close()
        self.result = "Created inventory file at /etc/tripleo/upgrade-inventory"
        self.changed = True
        return True


    def write_common_data(self, inventory_file, role):
        inventory_file.write('\n'
                             '[%s:vars]\n'
                             'ansible_ssh_user=heat-admin\n'
                             'ansible_become=true\n'
                             'ansible_become_user=root\n'
                             'ansible_become_method=sudo\n' % role)


    def write_service_list(self, inventory_file):
        # Add a role to a service
        # [keystone:children]
        # controller
        for role in self.tripleo_services:
            for service in self.tripleo_services[role]:
                inventory_file.write('\n[%s:children]\n' % service)
                inventory_file.write('%s\n' % role)


def main():
    module = AnsibleModule(argument_spec={})

    builder = BuildInventory()

    if not builder.read_heat_output('/tmp/upgrade-information',
                                    'heat_upgrade_data'):
        module.exit_json(failed=True, changed=builder.changed,
                         msg=builder.result)

    if not builder.read_heat_output('/tmp/node-information','heat_node_data'):
        module.exit_json(failed=True, changed=builder.changed,
                         msg=builder.result)

    if not builder.build_inventory_file():
        module.exit_json(failed=True, changed=builder.changed,
                         msg=builder.result)
    module.exit_json(changed=builder.changed, msg=builder.result)

from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()
