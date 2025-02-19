#!/usr/bin/env python
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# Copyright (C) 2020  Marius Rieder <marius.rieder@durchmesser.ch>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License;
# either version 2 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

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

    license_state, license_date, license_validity, license_used, license_total = section[int(item)]

    if license_state == 'Valid':
        summary_message = f'License is valid till {license_date}' if license_date else 'License has no expiration date'
        yield Result(state=State.OK, summary=summary_message)
    else:
        yield Result(state=State.CRIT, summary=f'License is {license_state}')

    license_validity = section[int(item)][2].strip()

    if not license_validity or license_validity in ['-1', '']:
        license_validity = None
    else:
        try:
            license_validity = float(license_validity)
            if license_validity < 0: 
                license_validity = None
        except ValueError:
            license_validity = None

    if license_validity is not None and license_validity > 0:
        label = 'Period of validity'
        validity_message = render.timespan(license_validity)
    else:
        label = 'License does not expire'
        validity_message = label

    yield Result(state=State.OK, summary=validity_message)

    # Handling license usage
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

    yield from check_levels(
        license_used,
        label="used",
        render_func=lambda v: f"{v:d}",
        levels_upper=levels,
        metric_name='licenses',
        boundaries=(0, int(license_total))
    )

check_plugin_veeam_o365jobs = CheckPlugin(
    name='veeam_o365licenses',
    service_name='VEEAM O365 License %s',
    discovery_function=discovery_veeam_o365licenses,
    check_function=check_veeam_o365licenses,
    check_ruleset_name='veeam_o365licenses',
    check_default_parameters={},
)
