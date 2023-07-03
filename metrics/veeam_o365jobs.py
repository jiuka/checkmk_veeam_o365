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
    MB
)


check_metrics['check_mk-veeam_o365jobs'] = {
    'transferred': {'name': 'veeam_o365jobs_transferred'},
    'duration': {'name': 'veeam_o365jobs_duration'},
    'items': {'name': 'veeam_o365jobs_items'},
    'age': {'name': 'veeam_o365jobs_age'},
}


metric_info['veeam_o365jobs_transferred'] = {
    'title': _('Data Transferred'),
    'unit': 'bytes',
    'color': '#00b336',
}

metric_info['veeam_o365jobs_duration'] = {
    'title': _('Job Duration'),
    'unit': 's',
    'color': '#00b336',
}

metric_info['veeam_o365jobs_items'] = {
    'title': _('Items Transferred'),
    'unit': 'count',
    'color': '#00b336',
}

metric_info['veeam_o365jobs_age'] = {
    'title': _('Time since last successfull run'),
    'unit': 's',
    'color': '#00b336',
}


graph_info['veeam_o365jobs_transferred'] = {
    'title': _('Veeam for Office 365 Job'),
    'metrics': [('veeam_o365jobs_transferred', 'area')],
    'range': (0, 'veeam_o365jobs_transferred:max'),
}

graph_info['veeam_o365jobs_duration'] = {
    'title': _('Veeam for Office 365 Job'),
    'metrics': [('veeam_o365jobs_duration', 'area')],
    'scalars': [
        'veeam_o365jobs_duration:warn',
        'veeam_o365jobs_duration:crit',
    ],
    'range': (0, 'veeam_o365jobs_duration:max'),
}

graph_info['veeam_o365jobs_items'] = {
    'title': _('Veeam for Office 365 Job'),
    'metrics': [('veeam_o365jobs_items', 'area')],
    'range': (0, 'veeam_o365jobs_items:max'),
}

graph_info['veeam_o365jobs_age'] = {
    'title': _('Veeam for Office 365 Job'),
    'metrics': [('veeam_o365jobs_age', 'area')],
    'range': (0, 'veeam_o365jobs_age:max'),
}


perfometer_info.append({
    'type': 'stacked',
    'perfometers': [{
        'type': 'logarithmic',
        'metric': 'veeam_o365jobs_transferred',
        'half_value': MB,
        'exponent': 2,
    }, {
        'type': 'logarithmic',
        'metric': 'veeam_o365jobs_duration',
        'half_value': 60,
        'exponent': 2
    }],
})
