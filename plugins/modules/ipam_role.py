#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2019, Mikhail Yohman (@FragmentedPacket)
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: ipam_role
short_description: Creates or removes ipam roles from Nautobot
description:
  - Creates or removes ipam roles from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Mikhail Yohman (@FragmentedPacket)
version_added: "1.0.0"
extends_documentation_fragment:
  - networktocode.nautobot.fragments.base
options:
  name:
    description:
      - Name of the ipam role to be created
    required: true
    type: str
    version_added: "3.0.0"
  slug:
    description:
      - The slugified version of the name or custom slug.
      - This is auto-generated following Nautobot rules if not provided
    required: false
    type: str
    version_added: "3.0.0"
  weight:
    description:
      - The weight of the ipam role to be created
    required: false
    type: int
    version_added: "3.0.0"
"""

EXAMPLES = r"""
- name: "Test Nautobot module"
  connection: local
  hosts: localhost
  gather_facts: False
  tasks:
    - name: Create ipam role within Nautobot with only required information
      networktocode.nautobot.ipam_role:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test IPAM Role
        state: present

    - name: Delete ipam role within nautobot
      networktocode.nautobot.ipam_role:
        url: http://nautobot.local
        token: thisIsMyToken
        name: Test IPAM Role
        state: absent
"""

RETURN = r"""
role:
  description: Serialized object as created or already existent within Nautobot
  returned: on creation
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""

from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import NAUTOBOT_ARG_SPEC
from ansible_collections.networktocode.nautobot.plugins.module_utils.ipam import (
    NautobotIpamModule,
    NB_IPAM_ROLES,
)
from ansible.module_utils.basic import AnsibleModule
from copy import deepcopy


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(
        dict(
            name=dict(required=True, type="str"),
            slug=dict(required=False, type="str"),
            weight=dict(required=False, type="int"),
        )
    )

    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)

    ipam_role = NautobotIpamModule(module, NB_IPAM_ROLES)
    ipam_role.run()


if __name__ == "__main__":  # pragma: no cover
    main()