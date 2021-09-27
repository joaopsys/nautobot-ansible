#!/usr/bin/python
# -*- coding: utf-8 -*-


from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = r"""
---
module: prefix
short_description: Creates or removes prefixes from Nautobot
description:
  - Creates or removes prefixes from Nautobot
notes:
  - Tags should be defined as a YAML list
  - This should be ran with connection C(local) and hosts C(localhost)
author:
  - Network to Code (@networktocode)
  - Anthony Ruhier (@Anthony25)
requirements:
  - pynautobot
version_added: "1.0.0"
options:
  url:
    description:
      - URL of the Nautobot instance resolvable by Ansible control host
    required: true
    type: str
  token:
    description:
      - The token created within Nautobot to authorize API access
    required: true
    type: str
  data:
    type: dict
    description:
      - (deprecated) In the next version of the modules the `data` option will be removed. All sub options will now be an option of the module.
      - Defines the prefix configuration
    suboptions:
      family:
        description:
          - Specifies which address family the prefix prefix belongs to
        required: false
        type: int
      prefix:
        description:
          - Required if state is C(present) and first_available is False. Will allocate or free this prefix.
        required: false
        type: raw
      parent:
        description:
          - Required if state is C(present) and first_available is C(yes). Will get a new available prefix in this parent prefix.
        required: false
        type: raw
      prefix_length:
        description:
          - |
            Required ONLY if state is C(present) and first_available is C(yes).
            Will get a new available prefix of the given prefix_length in this parent prefix.
        required: false
        type: int
      site:
        description:
          - Site that prefix is associated with
        required: false
        type: raw
      vrf:
        description:
          - VRF that prefix is associated with
        required: false
        type: raw
      tenant:
        description:
          - The tenant that the prefix will be assigned to
        required: false
        type: raw
      vlan:
        description:
          - The VLAN the prefix will be assigned to
        required: false
        type: raw
      status:
        description:
          - The status of the prefix
        required: false
        type: raw
      prefix_role:
        description:
          - The role of the prefix
        required: false
        type: raw
      is_pool:
        description:
          - All IP Addresses within this prefix are considered usable
        required: false
        type: bool
      description:
        description:
          - The description of the prefix
        required: false
        type: str
      tags:
        description:
          - Any tags that the prefix may need to be associated with
        required: false
        type: list
      custom_fields:
        description:
          - Must exist in Nautobot and in key/value format
        required: false
        type: dict
    required: true
  state:
    description:
      - Use C(present) or C(absent) for adding or removing.
    choices: [ absent, present ]
    default: present
    type: str
  first_available:
    description:
      - If C(yes) and state C(present), if an parent is given, it will get the
        first available prefix of the given prefix_length inside the given parent (and
        vrf, if given).
        Unused with state C(absent).
    default: false
    type: bool
  query_params:
    description:
      - This can be used to override the specified values in ALLOWED_QUERY_PARAMS that is defined
      - in plugins/module_utils/utils.py and provides control to users on what may make
      - an object unique in their environment.
    required: false
    type: list
    elements: str
  validate_certs:
    description:
      - If C(no), SSL certificates will not be validated. This should only be used on personally controlled sites using self-signed certificates.
    default: true
    type: raw
"""

EXAMPLES = r"""
- name: "Test Nautobot prefix module"
  connection: local
  hosts: localhost
  gather_facts: False

  tasks:
    - name: Create prefix within Nautobot with only required information
      networktocode.nautobot.prefix:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
          prefix: 10.156.0.0/19
          status: active
        state: present

    - name: Delete prefix within nautobot
      networktocode.nautobot.prefix:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
          prefix: 10.156.0.0/19
        state: absent

    - name: Create prefix with several specified options
      networktocode.nautobot.prefix:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
          family: 4
          prefix: 10.156.32.0/19
          site: Test Site
          vrf: Test VRF
          tenant: Test Tenant
          vlan:
            name: Test VLAN
            site: Test Site
            tenant: Test Tenant
            vlan_group: Test Vlan Group
          status: Reserved
          prefix_role: Network of care
          description: Test description
          is_pool: true
          tags:
            - Schnozzberry
        state: present

    - name: Get a new /24 inside 10.156.0.0/19 within Nautobot - Parent doesn't exist
      networktocode.nautobot.prefix:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
          parent: 10.156.0.0/19
          prefix_length: 24
        state: present
        first_available: yes

    - name: Create prefix within Nautobot with only required information
      networktocode.nautobot.prefix:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
          prefix: 10.156.0.0/19
        state: present

    - name: Get a new /24 inside 10.156.0.0/19 within Nautobot
      networktocode.nautobot.prefix:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
          parent: 10.156.0.0/19
          prefix_length: 24
        state: present
        first_available: yes

    - name: Get a new /24 inside 10.157.0.0/19 within Nautobot with additional values
      networktocode.nautobot.prefix:
        url: http://nautobot.local
        token: thisIsMyToken
        data:
          parent: 10.157.0.0/19
          prefix_length: 24
          vrf: Test VRF
          site: Test Site
        state: present
        first_available: yes
"""

RETURN = r"""
prefix:
  description: Serialized object as created or already existent within Nautobot
  returned: on creation
  type: dict
msg:
  description: Message indicating failure or info about what has been achieved
  returned: always
  type: str
"""


from ansible_collections.networktocode.nautobot.plugins.module_utils.utils import (
    NautobotAnsibleModule,
    NAUTOBOT_ARG_SPEC,
)
from ansible_collections.networktocode.nautobot.plugins.module_utils.ipam import (
    NautobotIpamModule,
    NB_PREFIXES,
)
from copy import deepcopy


def main():
    """
    Main entry point for module execution
    """
    argument_spec = deepcopy(NAUTOBOT_ARG_SPEC)
    argument_spec.update(
        dict(
            data=dict(
                type="dict",
                required=True,
                options=dict(
                    family=dict(required=False, type="int"),
                    prefix=dict(required=False, type="raw"),
                    parent=dict(required=False, type="raw"),
                    prefix_length=dict(required=False, type="int"),
                    site=dict(required=False, type="raw"),
                    vrf=dict(required=False, type="raw"),
                    tenant=dict(required=False, type="raw"),
                    vlan=dict(required=False, type="raw"),
                    status=dict(required=False, type="raw"),
                    prefix_role=dict(required=False, type="raw"),
                    is_pool=dict(required=False, type="bool"),
                    description=dict(required=False, type="str"),
                    tags=dict(required=False, type="list"),
                    custom_fields=dict(required=False, type="dict"),
                ),
            ),
            first_available=dict(required=False, type="bool", default=False),
        )
    )

    required_if = [
        ("state", "present", ["prefix", "parent", "status"], True),
        ("state", "absent", ["prefix"]),
        ("first_available", "yes", ["parent"]),
    ]

    module = NautobotAnsibleModule(
        argument_spec=argument_spec, supports_check_mode=True, required_if=required_if
    )

    prefix = NautobotIpamModule(module, NB_PREFIXES)
    prefix.run()


if __name__ == "__main__":  # pragma: no cover
    main()
