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

from cmk.gui.exceptions import MKUserError
from cmk.gui.i18n import _
from cmk.gui.plugins.wato.check_parameters.licenses import _vs_license
from cmk.gui.valuespec import (
        Age,
        Dictionary,
        TextAscii,
        Tuple,
)
from cmk.gui.plugins.wato import (
    CheckParameterRulespecWithItem,
    RulespecGroupCheckParametersApplications,
    rulespec_registry,
)


def _validate_tuple_decrease(value, varprefix):
    cur = value[0]
    for entry in value[1:]:
        if entry >= cur:
            raise MKUserError(varprefix,
                              _('Warning needs to be bigger then critical'))
        cur = entry


def _item_spec_veeam_o365licenses():
    return TextAscii(
        title=_('Veeam for Office365 Licenses number'),
        allow_empty=False,
        help=_('Number of thelicense service.')
    )


def _valuespec_spec_veeam_o365licenses():
    return Dictionary(
        elements=[
            ('validity',
             Tuple(
                 title=_('Certificate Age'),
                 help=_("Days until expiry of certificate"),
                 elements=[
                     Age(title=_("Warning at"),
                         display=['days'],
                         default_value=90*24*60*60),
                     Age(title=_("Critical at"),
                         display=['days'],
                         default_value=60*24*60*60),
                 ],
                 validate=_validate_tuple_decrease,
             )),
            ('license', _vs_license()),
        ],
    )


rulespec_registry.register(
    CheckParameterRulespecWithItem(
        check_group_name='veeam_o365licenses',
        group=RulespecGroupCheckParametersApplications,
        item_spec=_item_spec_veeam_o365licenses,
        parameter_valuespec=_valuespec_spec_veeam_o365licenses,
        title=lambda: _('Veeam for Office 365 licenses'),
    ))
