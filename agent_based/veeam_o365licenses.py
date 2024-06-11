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

# <<<veeam_o365licenses:sep(9) >>>
# Valid	28.06.2020 02:00:00	2592000	42	50000

from cmk.agent_based.v2 import (
    Service,
    Result,
    State,
    check_levels,
    render,
    CheckPlugin,
)


def discovery_veeam_o365licenses(section):
    for index, line in enumerate(section):
        yield Service(item=str(index))


def check_veeam_o365licenses(item, params, section):
    if int(item) >= len(section):
        return

    license_state, license_date, license_validity, \
        license_used, license_total = section[int(item)]

    if license_state == 'Valid':
        yield Result(state=State.OK, summary='License is vaild till %s' % license_date)
    else:
        yield Result(state=State.CRIT, summary='License is %s' % license_state)

    yield from check_levels(
        float(license_validity),
        levels_lower=params.get('validity', ('fixed', (0, 0))),
        label='Period of validity' if float(license_validity) > 0 else 'Expired since',
        render_func=lambda f: render.timespan(f if f > 0 else -f),
    )

    license_used = int(license_used)
    license_total = int(license_total)

    match params.get('licenses', None):
        case ('always_ok', None):
            levels = ('no_levels', None)
        case ('absolute', {'warn': warn, 'crit': crit}):
            levels = ('fixed', (license_total - warn, license_total - crit))
        case ('percentage', {'warn': warn, 'crit': crit}):
            levels = ('fixed', (int(license_total * (100 - warn) / 100), int(license_total * (100 - crit) / 100)))
        case _:
            levels = ('fixed', (int(license_total), int(license_total)))

    yield from check_levels(license_used,
                            label="used",
                            render_func=lambda v: f"{v:d}",
                            levels_upper=levels,
                            metric_name='licenses',
                            boundaries=(0, int(license_total)))


check_plugin_veeam_o365jobs = CheckPlugin(
    name='veeam_o365licenses',
    service_name = 'VEEAM O365 License %s',
    discovery_function=discovery_veeam_o365licenses,
    check_function=check_veeam_o365licenses,
    check_ruleset_name='veeam_o365licenses',
    check_default_parameters={},
)
