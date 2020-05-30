#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cmk.gui.i18n import _
from cmk.gui.valuespec import (
    Age,
    Dictionary,
    DropdownChoice,
    MonitoringState,
    TextAscii,
    TextUnicode,
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
                 title=_("Appearance of job"),
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
                 title=_("Duration"),
                 elements=[
                     Age(title=_("Warning at"),),
                     Age(title=_("Critical at"),),
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
                 help=_('Remap the job status to different monitoring states.'),
                 required_keys=[
                     'Success',
                     'Warning',
                     'Stopped',
                     'Failed',
                 ],
             )),
            ('jobId', TextUnicode(title=_('Job ID'))),
        ],
        help=_('This rule is used to configure thresholds Veeam for Office 365 jobs.'),
    )


rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name='veeam_o365jobs',
        group=RulespecGroupCheckParametersApplications,
        item_spec=_item_spec_veeam_o365jobs,
        parameter_valuespec=_parameter_valuespec_veeam_o365jobs,
        title=lambda: _("Veeam for Office 365 Job Levels"),
    ))
