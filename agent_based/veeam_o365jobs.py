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

# <<<veeam_o365jobs:sep(9) >>>
# 01234567-89ab-cdef-0123-456789abcdef  cmk.onmicrosoft.com Outlook Online  Success 29.05.2020 16:45:46 29.05.2020 16:47:55 128.7511818 191 142
# 12345678-9abc-def0-1234-56789abcdef0  cmk.onmicrosoft.com Outlook Online2  Failed 29.05.2020 16:45:46 29.05.2020 16:47:55 128.7511818

from dataclasses import dataclass
from typing import Optional
from .agent_based_api.v1 import (
    Service,
    Result,
    State,
    check_levels,
    render,
    register,
)
from .agent_based_api.v1.type_defs import StringTable

VEEAM_O365JOBS_CHECK_DEFAULT_PARAMETERS = {
    'states': {
        'Success': 0,
        'Warning': 1,
        'Stopped': 1,
        'Failed': 2,
    }
}


@dataclass
class VeeamO365Job:
    org: str
    name: str
    state: str
    duration: float
    objects: Optional[int] = None
    transferred: Optional[int] = None
    success_age: Optional[int] = None

    @property
    def name_short(self):
        return f"{self.org.replace('.onmicrosoft.com', '')} {self.name}"

    @property
    def name_full(self):
        return f"{self.org} {self.name}"


def parse_veeam_o365jobs(string_table: StringTable) -> dict[str, VeeamO365Job]:
    parsed = {}

    for item in string_table:
        try:
            job = VeeamO365Job(
                org=item[1],
                name=item[2],
                state=item[3],
                duration=float(item[6]),
            )
            if len(item) >= 9:
                job.objects = int(item[7]) if item[7].isnumeric() else None
                job.transferred = int(item[8]) if item[8].isnumeric() else None
            if len(item) >= 10:
                job.success_age = int(item[9]) if item[9].isnumeric() else None
            parsed[item[0]] = job
        except Exception:
            pass
    return parsed


register.agent_section(
    name='veeam_o365jobs',
    parse_function=parse_veeam_o365jobs,
)


def discovery_veeam_o365jobs(params, section):
    appearance = params.get('item_appearance', 'name')

    for id, job in section.items():
        name = job.name
        if appearance == 'short':
            name = job.name_short
        elif appearance == 'full':
            name = job.name_full
        yield Service(item=name, parameters={'jobId': id})


def check_veeam_o365jobs(item, params, section):
    if params.get('jobId', None) not in section:
        return
    job = section.get(params.get('jobId', None))

    if job.state == 'Running':
        yield from check_levels(
            float(job.duration),
            levels_upper=params.get('duration', None),
            label='Running since',
            render_func=render.timespan,
        )
    else:
        state = params.get('states').get(job.state, 3)
        yield Result(state=State(state), summary='Status: %s' % job.state)

        if job.objects is not None:
            yield from check_levels(
                int(job.objects),
                metric_name='items',
                label='Transferred Items',
            )

        if job.transferred is not None:
            yield from check_levels(
                float(job.transferred),
                metric_name='transferred',
                label='Transferred Data',
                render_func=render.bytes,
            )

        yield from check_levels(
            float(job.duration),
            metric_name='duration',
            levels_upper=params.get('duration', None),
            label='Backup duration',
            render_func=render.timespan,
        )

    if job.success_age is not None:
        yield from check_levels(
            value=int(job.success_age),
            metric_name='age',
            levels_upper=params.get('maxage', None),
            render_func=render.timespan,
            label='Last Success',
            notice_only=True,
        )


register.check_plugin(
    name = 'veeam_o365jobs',
    service_name = 'VEEAM O365 Job %s',
    discovery_ruleset_name='inventory_veeam_o365jobs_rules',
    discovery_ruleset_type=register.RuleSetType.MERGED,
    discovery_default_parameters={},
    discovery_function = discovery_veeam_o365jobs,
    check_function = check_veeam_o365jobs,
    check_ruleset_name='veeam_o365jobs',
    check_default_parameters=VEEAM_O365JOBS_CHECK_DEFAULT_PARAMETERS,
)
