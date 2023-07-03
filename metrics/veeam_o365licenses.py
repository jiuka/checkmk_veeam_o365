#!/usr/bin/python
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

from cmk.gui.plugins.metrics.utils import (
    check_metrics,
    metric_info,
    graph_info,
    perfometer_info,
)


check_metrics['check_mk-veeam_o365licenses'] = {
    'licenses': {
        'name': 'veeam_o365licenses_licenses'
    },
}

metric_info['veeam_o365licenses_licenses'] = {
    'title': _('Used licenses'),
    'unit': 'count',
    'color': '#00b336',
}

graph_info['veeam_o365licenses_licenses'] = {
    'title': _('Veeam for Office 365 licenses'),
    'metrics': [('veeam_o365licenses_licenses', 'area')],
    'scalars': [
        'veeam_o365licenses_licenses:warn',
        'veeam_o365licenses_licenses:crit',
        ('veeam_o365licenses_licenses:max#000000', 'Total licenses'),
    ],
    'range': (0, 'veeam_o365licenses_licenses:max'),
}

perfometer_info.append({
    'type': 'linear',
    'segments': ['veeam_o365licenses_licenses'],
    'total': 'veeam_o365licenses_licenses:max',
})
