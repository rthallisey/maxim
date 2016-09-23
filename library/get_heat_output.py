#!/usr/bin/env python


import subprocess


def main():
    module = AnsibleModule(argument_spec={})

    rc = subprocess.check_output('heat output-show overcloud EnabledServices > '
                          '/tmp/upgrade-information', shell=True)

    rc = subprocess.check_output('heat output-show overcloud RoleNodes > '
                                 '/tmp/node-information', shell=True)

    result = "Created '/tmp/upgrade-information' and '/tmp/node-information'"
    module.exit_json(changed=True, failed=False,  msg=result)

from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()
