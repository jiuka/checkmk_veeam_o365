#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# Copyright (C) 2020  Marius Rieder <marius.rieder@durchmesser.ch>
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

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Age,
    Dictionary,
    DropdownChoice,
    MonitoringState,
    TextAscii,
    Tuple,
)
from cmk.gui.plugins.wato import (
    CheckParameterRulespecWithItem,
    RulespecGroupCheckParametersApplications,
    RulespecGroupCheckParametersDiscovery,
    rulespec_registry,
    HostRulespec,
)


def _valuespec_inventory_veeam_o365jobs_rules():
    return Dictionary(
        title=_('Veeam for Office 365 Job Discovery'),
        elements=[
            ('item_appearance',
             DropdownChoice(
                 title=_('Appearance of job'),
                 help=_(
                     'This option lets Check_MK use either only the job name, '
                     'prepend it with the shortend org oder the full org.'),
                 choices=[
                     ('name', _('Use only the job name')),
                     ('short', _('Use the shortend org and the name')),
                     ('full', _('Use the full org and the name')),
                 ],
                 default_value='name',
             )),
        ],
        help=_('This rule can be used to control the inventory for Veeam for '
               'Office 365 Jobs. You can configure the service name to include'
               'the Organisation.'),
    )


rulespec_registry.register(
    HostRulespec(
        group=RulespecGroupCheckParametersDiscovery,
        name='inventory_veeam_o365jobs_rules',
        valuespec=_valuespec_inventory_veeam_o365jobs_rules,
    ))


def _item_spec_veeam_o365jobs():
    return TextAscii(
        title=_('Veeam for Office365 Job name'),
        help=_('Name of the jobs service.')
    )


def _parameter_valuespec_veeam_o365jobs():
    return Dictionary(
        title=_('Veem for Office 365 Jobs'),
        elements=[
            ('duration',
             Tuple(
                 title=_('Duration'),
                 elements=[
                     Age(title=_('Warning at'),),
                     Age(title=_('Critical at'),),
                 ],
                 help=_('Thresholds for duration of the job.'),
             )),
            ('states',
             Dictionary(
                 title=_('State mapping'),
                 elements=[
                     ('Success',
                      MonitoringState(
                          title=_('Success'),
                          default_value=0,
                      )),
                     ('Warning',
                      MonitoringState(
                          title=_('Warning'),
                          default_value=1,
                      )),
                     ('Stopped',
                      MonitoringState(
                          title=_('Stopped'),
                          default_value=1,
                      )),
                     ('Failed',
                      MonitoringState(
                          title=_('Failed'),
                          default_value=2,
                      )),
                 ],
                 help=_('Remap the job stat to different monitoring states.'),
                 required_keys=[
                     'Success',
                     'Warning',
                     'Stopped',
                     'Failed',
                 ],
             )),
        ],
        help=_('This rule configures thresholds Veeam for Office 365 jobs.'),
    )


rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name='veeam_o365jobs',
        group=RulespecGroupCheckParametersApplications,
        item_spec=_item_spec_veeam_o365jobs,
        parameter_valuespec=_parameter_valuespec_veeam_o365jobs,
        title=lambda: _('Veeam for Office 365 Job Levels'),
    ))
