#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2021, Cisco Systems
# GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
from ansible.plugins.action import ActionBase
try:
    from ansible_collections.ansible.utils.plugins.module_utils.common.argspec_validate import (
        AnsibleArgSpecValidator,
    )
except ImportError:
    ANSIBLE_UTILS_IS_INSTALLED = False
else:
    ANSIBLE_UTILS_IS_INSTALLED = True
from ansible.errors import AnsibleActionFail
from ansible_collections.cisco.meraki.plugins.plugin_utils.meraki import (
    MERAKI,
    meraki_argument_spec,
)

# Get common arguments specification
argument_spec = meraki_argument_spec()
# Add arguments specific for this module
argument_spec.update(dict(
    networkId=dict(type="str"),
    organizationId=dict(type="str"),
    configTemplateId=dict(type="str"),
    isBoundToConfigTemplate=dict(type="bool"),
    tags=dict(type="list"),
    tagsFilterType=dict(type="str"),
    perPage=dict(type="int"),
    total_pages=dict(type="int"),
    direction=dict(type="str"),
    startingAfter=dict(type="str"),
    endingBefore=dict(type="str"),
))

required_if = []
required_one_of = []
mutually_exclusive = []
required_together = []


class ActionModule(ActionBase):
    def __init__(self, *args, **kwargs):
        if not ANSIBLE_UTILS_IS_INSTALLED:
            raise AnsibleActionFail(
                "ansible.utils is not installed. Execute 'ansible-galaxy collection install ansible.utils'")
        super(ActionModule, self).__init__(*args, **kwargs)
        self._supports_async = False
        self._supports_check_mode = True
        self._result = None

    # Checks the supplied parameters against the argument spec for this module
    def _check_argspec(self):
        aav = AnsibleArgSpecValidator(
            data=self._task.args,
            schema=dict(argument_spec=argument_spec),
            schema_format="argspec",
            schema_conditionals=dict(
                required_if=required_if,
                required_one_of=required_one_of,
                mutually_exclusive=mutually_exclusive,
                required_together=required_together,
            ),
            name=self._task.action,
        )
        valid, errors, self._task.args = aav.validate()
        if not valid:
            raise AnsibleActionFail(errors)

    def get_object(self, params):
        new_object = {}
        if params.get("networkId") is not None:
            new_object["networkId"] = params.get(
                "networkId")
        return new_object

    def get_all(self, params):
        new_object = {}
        if params.get("organizationId") is not None:
            new_object["organizationId"] = params.get(
                "organizationId")
        if params.get("configTemplateId") is not None:
            new_object["configTemplateId"] = params.get(
                "configTemplateId")
        if params.get("isBoundToConfigTemplate") is not None:
            new_object["isBoundToConfigTemplate"] = params.get(
                "isBoundToConfigTemplate")
        if params.get("tags") is not None:
            new_object["tags"] = params.get(
                "tags")
        if params.get("tagsFilterType") is not None:
            new_object["tagsFilterType"] = params.get(
                "tagsFilterType")
        if params.get("perPage") is not None:
            new_object["perPage"] = params.get(
                "perPage")
        new_object['total_pages'] = params.get(
            "total_pages") or 1
        new_object['direction'] = params.get(
            "direction") or "next"
        if params.get("startingAfter") is not None:
            new_object["startingAfter"] = params.get(
                "startingAfter")
        if params.get("endingBefore") is not None:
            new_object["endingBefore"] = params.get(
                "endingBefore")

        return new_object

    def run(self, tmp=None, task_vars=None):
        self._task.diff = False
        self._result = super(ActionModule, self).run(tmp, task_vars)
        self._result["changed"] = False
        self._check_argspec()

        self._result.update(dict(meraki_response={}))

        meraki = MERAKI(params=self._task.args)

        id = self._task.args.get("networkId")
        if id:
            response = meraki.exec_meraki(
                family="organizationsnetworks",
                function='getNetwork',
                params=self.get_object(self._task.args),
            )
            self._result.update(dict(meraki_response=response))
            self._result.update(meraki.exit_json())
            return self._result
        if not id:
            response = meraki.exec_meraki(
                family="organizationsnetworks",
                function='getOrganizationNetworks',
                params=self.get_all(self._task.args),
            )
            self._result.update(dict(meraki_response=response))
            self._result.update(meraki.exit_json())
            return self._result
