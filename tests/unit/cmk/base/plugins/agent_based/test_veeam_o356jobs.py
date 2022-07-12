#!/usr/bin/env python3
# -*- encoding: utf-8; py-indent-offset: 4 -*-
#
# Copyright (C) 2021  Marius Rieder <marius.rieder@scs.ch>
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

import pytest  # type: ignore[import]
from cmk.base.plugins.agent_based.agent_based_api.v1 import (
    Metric,
    Result,
    Service,
    State,
)
from cmk.base.plugins.agent_based import veeam_o365jobs


@pytest.mark.parametrize('params, section, result', [
    ({}, [], []),
    (
        {},
        [
            ['01234567-89ab-cdef-0123-456789abcdef', 'cmk.onmicrosoft.com', 'Outlook Online', 'Success', '29.05.2020 16:45:46', '29.05.2020 16:47:55', '128.7511818', '191', '142'],
            ['12345678-9abc-def0-1234-56789abcdef0', 'cmk.onmicrosoft.com', 'Outlook Online2', 'Failed', '29.05.2020 16:45:46', '29.05.2020 16:47:55', '128.7511818']
        ],
        [
            Service(item='Outlook Online', parameters={'jobId': '01234567-89ab-cdef-0123-456789abcdef'}),
            Service(item='Outlook Online2', parameters={'jobId': '12345678-9abc-def0-1234-56789abcdef0'})
        ]
    ),
    (
        {'item_appearance': 'short'},
        [
            ['01234567-89ab-cdef-0123-456789abcdef', 'cmk.onmicrosoft.com', 'Outlook Online', 'Success', '29.05.2020 16:45:46', '29.05.2020 16:47:55', '128.7511818', '191', '142'],
            ['12345678-9abc-def0-1234-56789abcdef0', 'cmk.onmicrosoft.com', 'Outlook Online2', 'Failed', '29.05.2020 16:45:46', '29.05.2020 16:47:55', '128.7511818']
        ],
        [
            Service(item='cmk Outlook Online', parameters={'jobId': '01234567-89ab-cdef-0123-456789abcdef'}),
            Service(item='cmk Outlook Online2', parameters={'jobId': '12345678-9abc-def0-1234-56789abcdef0'})
        ]
    ),
    (
        {'item_appearance': 'full'},
        [
            ['01234567-89ab-cdef-0123-456789abcdef', 'cmk.onmicrosoft.com', 'Outlook Online', 'Success', '29.05.2020 16:45:46', '29.05.2020 16:47:55', '128.7511818', '191', '142'],
            ['12345678-9abc-def0-1234-56789abcdef0', 'cmk.onmicrosoft.com', 'Outlook Online2', 'Failed', '29.05.2020 16:45:46', '29.05.2020 16:47:55', '128.7511818']
        ],
        [
            Service(item='cmk.onmicrosoft.com Outlook Online', parameters={'jobId': '01234567-89ab-cdef-0123-456789abcdef'}),
            Service(item='cmk.onmicrosoft.com Outlook Online2', parameters={'jobId': '12345678-9abc-def0-1234-56789abcdef0'})
        ]
    ),
])
def test_discovery_veeam_o365jobs(params, section, result):
    assert list(veeam_o365jobs.discovery_veeam_o365jobs(params, section)) == result


@pytest.mark.parametrize('item, params, section, result', [
    ('', {}, [], []),
    (
        'cmk.onmicrosoft.com Outlook Online', {'jobId': '01234567-89ab-cdef-0123-456789abcdef'},
        [
            ['01234567-89ab-cdef-0123-456789abcdef', 'cmk.onmicrosoft.com', 'Outlook Online', 'Success', '29.05.2020 16:45:46', '29.05.2020 16:47:55', '128.7511818', '191', '142'],
            ['12345678-9abc-def0-1234-56789abcdef0', 'cmk.onmicrosoft.com', 'Outlook Online2', 'Failed', '29.05.2020 16:45:46', '29.05.2020 16:47:55', '128.7511818']
        ],
        [
            Result(state=State.OK, summary='Status: Success'),
            Result(state=State.OK, summary='Transferred Items: 191.00'),
            Metric('transferred', 191.0),
            Result(state=State.OK, summary='Transferred Data: 142 B'),
            Metric('items', 142.0),
            Result(state=State.OK, summary='Backup duration: 2 minutes 9 seconds'),
            Metric('duration', 128.7511818),
        ]
    ),
    (
        'cmk.onmicrosoft.com Outlook Online', {'jobId': '12345678-9abc-def0-1234-56789abcdef0'},
        [
            ['01234567-89ab-cdef-0123-456789abcdef', 'cmk.onmicrosoft.com', 'Outlook Online', 'Success', '29.05.2020 16:45:46', '29.05.2020 16:47:55', '128.7511818', '191', '142'],
            ['12345678-9abc-def0-1234-56789abcdef0', 'cmk.onmicrosoft.com', 'Outlook Online2', 'Failed', '29.05.2020 16:45:46', '29.05.2020 16:47:55', '128.7511818']
        ],
        [
            Result(state=State.CRIT, summary='Status: Failed'),
            Result(state=State.OK, summary='Backup duration: 2 minutes 9 seconds'),
            Metric('duration', 128.7511818),
        ]
    ),
    (
        'cmk.onmicrosoft.com Outlook Online', {'jobId': '12345678-9abc-def0-1234-56789abcdef0', 'duration': (120, 300)},
        [
            ['01234567-89ab-cdef-0123-456789abcdef', 'cmk.onmicrosoft.com', 'Outlook Online', 'Success', '29.05.2020 16:45:46', '29.05.2020 16:47:55', '128.7511818', '191', '142'],
            ['12345678-9abc-def0-1234-56789abcdef0', 'cmk.onmicrosoft.com', 'Outlook Online2', 'Failed', '29.05.2020 16:45:46', '29.05.2020 16:47:55', '128.7511818']
        ],
        [
            Result(state=State.CRIT, summary='Status: Failed'),
            Result(state=State.WARN, summary='Backup duration: 2 minutes 9 seconds (warn/crit at 2 minutes 0 seconds/5 minutes 0 seconds)'),
            Metric('duration', 128.7511818, levels=(120.0, 300.0)),
        ]
    ),
    (
        'cmk.onmicrosoft.com Outlook Online',
        {
            'jobId': '12345678-9abc-def0-1234-56789abcdef0',
            'states': {
                'Success': 0,
                'Warning': 1,
                'Stopped': 1,
                'Failed': 0,
            }
        },
        [
            ['01234567-89ab-cdef-0123-456789abcdef', 'cmk.onmicrosoft.com', 'Outlook Online', 'Success', '29.05.2020 16:45:46', '29.05.2020 16:47:55', '128.7511818', '191', '142'],
            ['12345678-9abc-def0-1234-56789abcdef0', 'cmk.onmicrosoft.com', 'Outlook Online2', 'Failed', '29.05.2020 16:45:46', '29.05.2020 16:47:55', '128.7511818']
        ],
        [
            Result(state=State.OK, summary='Status: Failed'),
            Result(state=State.OK, summary='Backup duration: 2 minutes 9 seconds'),
            Metric('duration', 128.7511818),
        ]
    ),
])
def test_check_veeam_o365jobs(item, params, section, result):
    fullparams = veeam_o365jobs.VEEAM_O365JOBS_CHECK_DEFAULT_PARAMETERS.copy()
    fullparams.update(params)
    assert list(veeam_o365jobs.check_veeam_o365jobs(item, fullparams, section)) == result
