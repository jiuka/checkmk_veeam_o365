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

from .agent_based_api.v1 import (
    Service,
    Result,
    State,
    check_levels,
    render,
    register,
)

VEEAM_O365JOBS_CHECK_DEFAULT_PARAMETERS = {
    'states': {
        'Success': 0,
        'Warning': 1,
        'Stopped': 1,
        'Failed': 2,
    }
}


def discovery_veeam_o365jobs(params, section):
    appearance = params.get('item_appearance', 'name')

    for line in section:
        name = line[2]
        if appearance == 'short':
            name = '%s %s' % (line[1].replace('.onmicrosoft.com', ''), line[2])
        elif appearance == 'full':
            name = '%s %s' % (line[1], line[2])
        yield Service(item=name, parameters={'jobId': line[0]})


def check_veeam_o365jobs(item, params, section):
    for line in section:
        if line[0] != params['jobId']:
            continue

        job_org, job_name, job_state, \
            job_creation_time, job_end_time, job_duration = line[1:7]
        job_objects = job_transferred = 0
        if len(line) >= 9:
            job_objects, job_transferred = line[7:9]

        if job_state in ['Running']:
            yield Result(state=State.OK, summary='Running since %s (current state is: %s)' % (job_creation_time, job_state))
            return

        state = params.get('states').get(job_state, 3)
        yield Result(state=State(state), summary='Status: %s' % job_state)

        if int(job_objects):
            yield from check_levels(
                int(job_objects),
                metric_name='transferred',
                label='Transferred Items',
            )

        if float(job_transferred):
            yield from check_levels(
                float(job_transferred),
                metric_name='items',
                label='Transferred Data',
                render_func=render.bytes,
            )

        yield from check_levels(
            float(job_duration),
            metric_name='duration',
            levels_upper=params.get('duration', None),
            label='Backup duration',
            render_func=render.timespan,
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
