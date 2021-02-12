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

from .agent_based_api.v1 import (
    Service,
    Result,
    State,
    check_levels,
    render,
    Metric,
    register,
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
        levels_lower=params.get('validity', None),
        label='Period of validityt',
        render_func=render.timespan,
    )

    license_params = params.get('licenses', None)

    if license_params is False:
        license_warn = None
        license_crit = None
    elif not license_params:
        license_warn = int(license_total)
        license_crit = int(license_total)
    elif isinstance(license_params[0], int):
        license_warn = max(0, int(license_total) - license_params[0])
        license_crit = max(0, int(license_total) - license_params[1])
    else:
        license_warn = int(license_total) * (1 - license_params[0] / 100.0)
        license_crit = int(license_total) * (1 - license_params[1] / 100.0)

    yield Metric('licenses',
                 int(license_used),
                 levels=(license_warn, license_crit),
                 boundaries=(0, int(license_total)))

    if int(license_used) <= int(license_total):
        infotext = 'used %d out of %d licenses' % (int(license_used), int(license_total))
    else:
        infotext = 'used %d licenses, but you have only %d' % (int(license_used), int(license_total))

    if license_crit is not None and int(license_used) >= license_crit:
        status = State.CRIT
    elif license_warn is not None and int(license_used) >= license_warn:
        status = State.WARN
    else:
        status = State.OK

    if license_crit is not None:
        infotext += ' (warn/crit at %d/%d)' % (license_warn, license_crit)

    yield Result(state=status, summary=infotext)


register.check_plugin(
    name = 'veeam_o365licenses',
    service_name = 'VEEAM O365 License %s',
    discovery_function = discovery_veeam_o365licenses,
    check_function = check_veeam_o365licenses,
    check_ruleset_name='veeam_o365licenses',
    check_default_parameters={},
)
