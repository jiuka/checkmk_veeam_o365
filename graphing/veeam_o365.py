#!/usr/bin/python
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

from cmk.graphing.v1 import (
    graphs as g,
    metrics as m,
    perfometers as p,
    translations as t,
)

translation_veeam_o365jobs = t.Translation(
    name='veeam_o365jobs',
    check_commands=[t.PassiveCheck('veeam_o365jobs')],
    translations={
        'transferred': t.RenameTo('veeam_o365jobs_transferred'),
        'duration': t.RenameTo('veeam_o365jobs_duration'),
        'items': t.RenameTo('veeam_o365jobs_items'),
        'age': t.RenameTo('veeam_o365jobs_age'),
    }
)

translation_veeam_o365licenses = t.Translation(
    name='veeam_o365licenses',
    check_commands=[t.PassiveCheck('veeam_o365licenses')],
    translations={
        'licenses': t.RenameTo('veeam_o365licenses_licenses'),
    }
)

metric_veeam_o365jobs_transferred = m.Metric(
    name='veeam_o365jobs_transferred',
    title=m.Title('Data Transferred'),
    unit=m.Unit(m.IECNotation("bits")),
    color=m.Color.GREEN,
)

metric_veeam_o365jobs_duration = m.Metric(
    name='veeam_o365jobs_duration',
    title=m.Title('Job Duration'),
    unit=m.Unit(m.TimeNotation()),
    color=m.Color.GREEN,
)

metric_veeam_o365jobs_items = m.Metric(
    name='veeam_o365jobs_items',
    title=m.Title('Items Transferred'),
    unit=m.Unit(m.DecimalNotation(""), m.StrictPrecision(0)),
    color=m.Color.GREEN,
)

metric_veeam_o365licenses_licenses = m.Metric(
    name='veeam_o365licenses_licenses',
    title=m.Title('Used licenses'),
    unit=m.Unit(m.DecimalNotation(""), m.StrictPrecision(0)),
    color=m.Color.GREEN,
)

graph_veeam_o365jobs_transferred = g.Graph(
    name='veeam_o365jobs_transferred',
    title=g.Title('Veeam for Office 365 Job'),
    minimal_range=g.MinimalRange(0, m.MaximumOf('veeam_o365jobs_transferred', m.Color.BLACK)),
    compound_lines=['veeam_o365jobs_transferred'],
    simple_lines=[
        m.WarningOf('veeam_o365jobs_transferred'),
        m.CriticalOf('veeam_o365jobs_transferred'),
    ]
)

graph_veeam_o365jobs_duration = g.Graph(
    name='veeam_o365jobs_duration',
    title=g.Title('Veeam for Office 365 Job'),
    minimal_range=g.MinimalRange(0, m.MaximumOf('veeam_o365jobs_duration', m.Color.BLACK)),
    compound_lines=['veeam_o365jobs_duration'],
    simple_lines=[
        m.WarningOf('veeam_o365jobs_duration'),
        m.CriticalOf('veeam_o365jobs_duration'),
    ]
)

graph_veeam_o365jobs_items = g.Graph(
    name='veeam_o365jobs_items',
    title=g.Title('Veeam for Office 365 Job'),
    minimal_range=g.MinimalRange(0, m.MaximumOf('veeam_o365jobs_items', m.Color.BLACK)),
    compound_lines=['veeam_o365jobs_items'],
    simple_lines=[
        m.WarningOf('veeam_o365jobs_items'),
        m.CriticalOf('veeam_o365jobs_items'),
    ]
)

graph_veeam_o365licenses_licenses = g.Graph(
    name='veeam_o365licenses_licenses',
    title=g.Title('Veeam for Office 365 licenses'),
    minimal_range=g.MinimalRange(0, m.MaximumOf('veeam_o365licenses_licenses', m.Color.BLACK)),
    compound_lines=['veeam_o365licenses_licenses'],
    simple_lines=[
        m.WarningOf('veeam_o365licenses_licenses'),
        m.CriticalOf('veeam_o365licenses_licenses'),
        m.MaximumOf('veeam_o365licenses_licenses', m.Color.BLACK)
    ]
)

perfometer_veeam_o365jobs = p.Stacked(
    name='veeam_o365jobs',
    upper=p.Perfometer(
        name='veeam_o365jobs_transferred',
        focus_range=p.FocusRange(p.Closed(0), p.Open(100)),
        segments=['veeam_o365jobs_transferred'],
    ),
    lower=p.Perfometer(
        name='veeam_o365jobs_duration',
        focus_range=p.FocusRange(p.Closed(0), p.Open(100)),
        segments=['veeam_o365jobs_duration'],
    ),
)

perfometer_veeam_o365licenses_licenses = p.Perfometer(
    name='veeam_o365licenses_licenses',
    focus_range=p.FocusRange(p.Closed(0), p.Open(m.MaximumOf('veeam_o365licenses_licenses', m.Color.BLACK))),
    segments=['veeam_o365licenses_licenses'],
)
