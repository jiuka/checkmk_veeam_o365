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

from cmk.rulesets.v1 import Help, Title, Message, Label
from cmk.rulesets.v1.form_specs import (
    DictElement,
    Dictionary,
    InputHint,
    LevelDirection,
    migrate_to_integer_simple_levels,
    migrate_to_float_simple_levels,
    SimpleLevels,
    CascadingSingleChoice,
    CascadingSingleChoiceElement,
    TimeMagnitude,
    TimeSpan,
    Integer,
    Percentage,
    FixedValue,
    validators,
    ServiceState,
    DefaultValue,
    String,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, Topic, HostAndItemCondition


def crit_lower_then_warn(value):
    if value['crit'] >= value['warn']:
        raise validators.ValidationError(Message("The critical level needs to be less or equal then the warning."))


def migrate_to_level_dict(value):
    if isinstance(value, tuple):
        return dict(warn=value[0], crit=value[1])
    return value


def _parameter_form_veeam_o365jobs():
    return Dictionary(
        elements={
            'duration': DictElement(
                parameter_form=SimpleLevels(
                    title=Title('Duration'),
                    help_text=Help('Thresholds for duration of the job.'),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=TimeSpan(
                        displayed_magnitudes=[TimeMagnitude.DAY, TimeMagnitude.HOUR, TimeMagnitude.MINUTE]
                    ),
                    migrate=migrate_to_float_simple_levels,
                    prefill_fixed_levels=InputHint(value=(1800, 3600)),
                ),
                required=False,
            ),
            'states': DictElement(
                parameter_form=Dictionary(
                    title=Title('State mapping'),
                    help_text=Help('Remap the job stat to different monitoring states.'),
                    elements={
                        'Success': DictElement(
                            parameter_form=ServiceState(
                                title=Title('Success'),
                                prefill=DefaultValue(0),
                            ),
                            required=True,
                        ),
                        'Warning': DictElement(
                            parameter_form=ServiceState(
                                title=Title('Warning'),
                                prefill=DefaultValue(1),
                            ),
                            required=True,
                        ),
                        'Stopped': DictElement(
                            parameter_form=ServiceState(
                                title=Title('Stopped'),
                                prefill=DefaultValue(1),
                            ),
                            required=True,
                        ),
                        'Failed': DictElement(
                            parameter_form=ServiceState(
                                title=Title('Failed'),
                                prefill=DefaultValue(2),
                            ),
                            required=True,
                        ),
                    }
                ),
                required=False,
            ),
            'success_maxage': DictElement(
                parameter_form=SimpleLevels(
                    title=Title('Maximal time since last successfull run'),
                    help_text=Help('Thresholds for last successfull run.'),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=TimeSpan(
                        displayed_magnitudes=[TimeMagnitude.DAY, TimeMagnitude.HOUR, TimeMagnitude.MINUTE]
                    ),
                    migrate=migrate_to_float_simple_levels,
                    prefill_fixed_levels=InputHint(value=(86400, 172800)),
                ),
                required=False,
            ),
            'jobId': DictElement(
                parameter_form=String(
                    title=Title('Veeam office 365 Job'),
                ),
                required=False,
                render_only=True,
            ),
        }
    )


rule_spec_veeam_o365jobs = CheckParameters(
    name='veeam_o365jobs',
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_form_veeam_o365jobs,
    title=Title('Veeam for Office 365 Job Levels'),
    help_text=Help('This rule configures thresholds Veeam for Office 365 jobs.'),
    condition=HostAndItemCondition(item_title=Title('Veeam for Office365 Job name')),
)


def _parameter_form_veeam_o365licenses():
    return Dictionary(
        elements={
            'validity': DictElement(
                parameter_form=SimpleLevels(
                    title=Title('License term'),
                    help_text=Help('Days until expiry of the license'),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=TimeSpan(
                        displayed_magnitudes=[TimeMagnitude.DAY]
                    ),
                    migrate=migrate_to_integer_simple_levels,
                    prefill_fixed_levels=InputHint(value=(30, 20)),
                ),
                required=False,
            ),
            'licenses': DictElement(
                parameter_form=CascadingSingleChoice(
                    title=Title("Levels for Number of Licenses"),
                    elements=[
                        CascadingSingleChoiceElement(
                            name="absolute",
                            title=Title('Absolute levels for unused licenses'),
                            parameter_form=Dictionary(
                                elements={
                                    "warn": DictElement(
                                        parameter_form=Integer(
                                            label=Label('Warning below'),
                                            unit_symbol='unused license',
                                            prefill=InputHint(5),
                                        ),
                                        required=True,
                                    ),
                                    "crit": DictElement(
                                        parameter_form=Integer(
                                            label=Label('Critical below'),
                                            unit_symbol='unused license',
                                            prefill=InputHint(0),
                                        ),
                                        required=True,
                                    )
                                },
                                custom_validate=[
                                    crit_lower_then_warn
                                ],
                                migrate=migrate_to_level_dict,
                            )
                        ),
                        CascadingSingleChoiceElement(
                            name="percentage",
                            title=Title('Percentual levels for unused licenses'),
                            parameter_form=Dictionary(
                                elements={
                                    "warn": DictElement(
                                        parameter_form=Percentage(
                                            label=Label('Warning below'),
                                            prefill=InputHint(10.0),
                                        ),
                                        required=True,
                                    ),
                                    "crit": DictElement(
                                        parameter_form=Percentage(
                                            label=Label('Critical below'),
                                            prefill=InputHint(0.0),
                                        ),
                                        required=True,
                                    )
                                },
                                custom_validate=[
                                    crit_lower_then_warn
                                ],
                                migrate=migrate_to_level_dict,
                            )
                        ),
                        CascadingSingleChoiceElement(
                            name='always_ok',
                            title=Title('Always be OK'),
                            parameter_form=FixedValue(value=False),
                        ),
                        CascadingSingleChoiceElement(
                            name='crit_on_all',
                            title=Title('Go critical if all licenses are used'),
                            parameter_form=FixedValue(value=None),
                        ),
                    ],
                    prefill='crit_on_all',
                ),
                required=True,
            ),
        },
    )


rule_spec_veeam_o365licenses = CheckParameters(
    name='veeam_o365licenses',
    topic=Topic.APPLICATIONS,
    parameter_form=_parameter_form_veeam_o365licenses,
    title=Title('Veeam for Office 365 licenses'),
    help_text=Help('This rule configures thresholds Veeam for Office 365 Licenses.'),
    condition=HostAndItemCondition(item_title=Title('Veeam for Office365 Licenses number')),
)
