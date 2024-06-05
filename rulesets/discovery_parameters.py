#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# Copyright (C) 2020-2024  Marius Rieder <marius.rieder@durchmesser.ch>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from cmk.rulesets.v1 import Help, Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    Dictionary,
    SingleChoice,
    SingleChoiceElement,
)
from cmk.rulesets.v1.rule_specs import DiscoveryParameters, Topic, HostCondition


def _parameter_form_veeam_o365jobs_discovery():
    return Dictionary(
        elements={
            'item_appearance': SingleChoice(
                title=Title('Appearance of job'),
                help_text=Help('This option lets Check_MK use either only the job name, '
                               'prepend it with the shortend org oder the full org.'),
                elements=[
                    SingleChoiceElement(name='name', title=Title('Use only the job name')),
                    SingleChoiceElement(name='short', title=Title('Use the shortend org and the name')),
                    SingleChoiceElement(name='full', title=Title('Use the full org and the name')),
                ],
                prefill=DefaultValue('name'),
            )
        },
    )


rule_spec_inventory_veeam_o365jobs_rules = DiscoveryParameters(
    name='veeam_o365jobs',
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_form_veeam_o365jobs_discovery,
    title=Title('Veeam for Office 365 Job Discovery'),
    help_text=Help('This rule can be used to control the inventory for Veeam for '
                   'Office 365 Jobs. You can configure the service name to include'
                   'the Organisation.'),
    condition=HostCondition(),
)
