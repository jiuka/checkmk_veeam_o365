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
from cmk.agent_based.v2 import (
    Metric,
    Result,
    Service,
    State,
)
from cmk_addons.plugins.veeam_o365.agent_based import veeam_o365jobs

EXAMPLE_STRING_TABLE = [
    ['01234567-89ab-cdef-0123-456789abcold', 'cmk.onmicrosoft.com', 'Outlook Old Online', 'Success', '29.05.2020 16:45:46', '29.05.2020 16:47:55', '128.7511818', '191', '142'],
    ['12345678-9abc-def0-1234-56789abcdold', 'cmk.onmicrosoft.com', 'Outlook Old Online2', 'Failed', '29.05.2020 16:45:46', '29.05.2020 16:47:55', '128.7511818'],
    ['01234567-89ab-cdef-0123-456789abcdef', 'cmk.onmicrosoft.com', 'Outlook Online', 'Success', '29.05.2020 16:45:46', '29.05.2020 16:47:55', '128.7511818', '191', '142', '3641'],
    ['12345678-9abc-def0-1234-56789abcdef0', 'cmk.onmicrosoft.com', 'Outlook Online2', 'Failed', '29.05.2020 16:45:46', '29.05.2020 16:47:55', '128.7511818', '', '', '90041'],
    ['23456789-abcd-ef01-2345-6789abcdef01', 'cmk.onmicrosoft.com', 'Outlook Online3', 'Running', '29.05.2020 16:45:46', '31.12.9999 23:59:59', '314', '0', '28058', '90041'],
]
EXAMPLE_SECTION = {
    '01234567-89ab-cdef-0123-456789abcold': veeam_o365jobs.VeeamO365Job(org='cmk.onmicrosoft.com', name='Outlook Old Online', state='Success', duration=128.7511818, objects=191, transferred=142),
    '12345678-9abc-def0-1234-56789abcdold': veeam_o365jobs.VeeamO365Job(org='cmk.onmicrosoft.com', name='Outlook Old Online2', state='Failed', duration=128.7511818),
    '01234567-89ab-cdef-0123-456789abcdef': veeam_o365jobs.VeeamO365Job(org='cmk.onmicrosoft.com', name='Outlook Online', state='Success', duration=128.7511818, objects=191, transferred=142, success_age=3641),
    '12345678-9abc-def0-1234-56789abcdef0': veeam_o365jobs.VeeamO365Job(org='cmk.onmicrosoft.com', name='Outlook Online2', state='Failed', duration=128.7511818, objects=None, transferred=None, success_age=90041),
    '23456789-abcd-ef01-2345-6789abcdef01': veeam_o365jobs.VeeamO365Job(org='cmk.onmicrosoft.com', name='Outlook Online3', state='Running', duration=314, objects=0, transferred=28058, success_age=90041),
}


@pytest.mark.parametrize('string_table, result', [
    ([], {}),
    (
        EXAMPLE_STRING_TABLE,
        EXAMPLE_SECTION
    ),
])
def test_parse_win_scheduled_task(string_table, result):
    assert veeam_o365jobs.parse_veeam_o365jobs(string_table) == result


@pytest.mark.parametrize('params, section, result', [
    ({}, {}, []),
    (
        {}, EXAMPLE_SECTION,
        [
            Service(item='Outlook Old Online', parameters={'jobId': '01234567-89ab-cdef-0123-456789abcold'}),
            Service(item='Outlook Old Online2', parameters={'jobId': '12345678-9abc-def0-1234-56789abcdold'}),
            Service(item='Outlook Online', parameters={'jobId': '01234567-89ab-cdef-0123-456789abcdef'}),
            Service(item='Outlook Online2', parameters={'jobId': '12345678-9abc-def0-1234-56789abcdef0'}),
            Service(item='Outlook Online3', parameters={'jobId': '23456789-abcd-ef01-2345-6789abcdef01'}),
        ]
    ),
    (
        {'item_appearance': 'short'}, EXAMPLE_SECTION,
        [
            Service(item='cmk Outlook Old Online', parameters={'jobId': '01234567-89ab-cdef-0123-456789abcold'}),
            Service(item='cmk Outlook Old Online2', parameters={'jobId': '12345678-9abc-def0-1234-56789abcdold'}),
            Service(item='cmk Outlook Online', parameters={'jobId': '01234567-89ab-cdef-0123-456789abcdef'}),
            Service(item='cmk Outlook Online2', parameters={'jobId': '12345678-9abc-def0-1234-56789abcdef0'}),
            Service(item='cmk Outlook Online3', parameters={'jobId': '23456789-abcd-ef01-2345-6789abcdef01'}),
        ]
    ),
    (
        {'item_appearance': 'full'}, EXAMPLE_SECTION,
        [
            Service(item='cmk.onmicrosoft.com Outlook Old Online', parameters={'jobId': '01234567-89ab-cdef-0123-456789abcold'}),
            Service(item='cmk.onmicrosoft.com Outlook Old Online2', parameters={'jobId': '12345678-9abc-def0-1234-56789abcdold'}),
            Service(item='cmk.onmicrosoft.com Outlook Online', parameters={'jobId': '01234567-89ab-cdef-0123-456789abcdef'}),
            Service(item='cmk.onmicrosoft.com Outlook Online2', parameters={'jobId': '12345678-9abc-def0-1234-56789abcdef0'}),
            Service(item='cmk.onmicrosoft.com Outlook Online3', parameters={'jobId': '23456789-abcd-ef01-2345-6789abcdef01'}),
        ]
    ),
])
def test_discovery_veeam_o365jobs(params, section, result):
    assert list(veeam_o365jobs.discovery_veeam_o365jobs(params, section)) == result


@pytest.mark.parametrize('item, params, result', [
    ('', {}, []),
    (
        'cmk.onmicrosoft.com Outlook Online', {'jobId': '01234567-89ab-cdef-0123-456789abcdef'},
        [
            Result(state=State.OK, summary='Status: Success'),
            Result(state=State.OK, summary='Transferred Items: 191.00'),
            Metric('items', 191.0),
            Result(state=State.OK, summary='Transferred Data: 142 B'),
            Metric('transferred', 142.0),
            Result(state=State.OK, summary='Backup duration: 2 minutes 9 seconds'),
            Metric('duration', 128.7511818),
            Result(state=State.OK, notice='Last Success: 1 hour 0 minutes'),
            Metric('age', 3641.0),
        ]
    ),
    (
        'cmk.onmicrosoft.com Outlook Old Online', {'jobId': '01234567-89ab-cdef-0123-456789abcold'},
        [
            Result(state=State.OK, summary='Status: Success'),
            Result(state=State.OK, summary='Transferred Items: 191.00'),
            Metric('items', 191.0),
            Result(state=State.OK, summary='Transferred Data: 142 B'),
            Metric('transferred', 142.0),
            Result(state=State.OK, summary='Backup duration: 2 minutes 9 seconds'),
            Metric('duration', 128.7511818),
        ]
    ),
    (
        'cmk.onmicrosoft.com Outlook Online', {'jobId': '12345678-9abc-def0-1234-56789abcdef0'},
        [
            Result(state=State.CRIT, summary='Status: Failed'),
            Result(state=State.OK, summary='Backup duration: 2 minutes 9 seconds'),
            Metric('duration', 128.7511818),
            Result(state=State.OK, notice='Last Success: 1 day 1 hour'),
            Metric('age', 90041.0),
        ]
    ),
    (
        'cmk.onmicrosoft.com Outlook Online', {'jobId': '12345678-9abc-def0-1234-56789abcdef0', 'duration': ('fixed', (120, 300))},
        [
            Result(state=State.CRIT, summary='Status: Failed'),
            Result(state=State.WARN, summary='Backup duration: 2 minutes 9 seconds (warn/crit at 2 minutes 0 seconds/5 minutes 0 seconds)'),
            Metric('duration', 128.7511818, levels=(120.0, 300.0)),
            Result(state=State.OK, notice='Last Success: 1 day 1 hour'),
            Metric('age', 90041.0),
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
            Result(state=State.OK, summary='Status: Failed'),
            Result(state=State.OK, summary='Backup duration: 2 minutes 9 seconds'),
            Metric('duration', 128.7511818),
            Result(state=State.OK, notice='Last Success: 1 day 1 hour'),
            Metric('age', 90041.0),
        ]
    ),
    (
        'cmk.onmicrosoft.com Outlook Online3', {'jobId': '23456789-abcd-ef01-2345-6789abcdef01'},
        [
            Result(state=State.OK, summary='Running since: 5 minutes 14 seconds'),
            Result(state=State.OK, notice='Last Success: 1 day 1 hour'),
            Metric('age', 90041.0),
        ]
    ),
    (
        'cmk.onmicrosoft.com Outlook Online3', {'jobId': '23456789-abcd-ef01-2345-6789abcdef01', 'duration': ('fixed', (500, 600))},
        [
            Result(state=State.OK, summary='Running since: 5 minutes 14 seconds'),
            Result(state=State.OK, notice='Last Success: 1 day 1 hour'),
            Metric('age', 90041.0),
        ]
    ),
    (
        'cmk.onmicrosoft.com Outlook Online3', {'jobId': '23456789-abcd-ef01-2345-6789abcdef01', 'duration': ('fixed', (120, 600))},
        [
            Result(state=State.WARN, summary='Running since: 5 minutes 14 seconds (warn/crit at 2 minutes 0 seconds/10 minutes 0 seconds)'),
            Result(state=State.OK, notice='Last Success: 1 day 1 hour'),
            Metric('age', 90041.0),
        ]
    ),
    (
        'cmk.onmicrosoft.com Outlook Online3', {'jobId': '23456789-abcd-ef01-2345-6789abcdef01', 'duration': ('fixed', (120, 300))},
        [
            Result(state=State.CRIT, summary='Running since: 5 minutes 14 seconds (warn/crit at 2 minutes 0 seconds/5 minutes 0 seconds)'),
            Result(state=State.OK, notice='Last Success: 1 day 1 hour'),
            Metric('age', 90041.0),
        ]
    ),
    (
        'cmk.onmicrosoft.com Outlook Online', {'jobId': '01234567-89ab-cdef-0123-456789abcdef', 'success_maxage': ('fixed', (1800, 504000))},
        [
            Result(state=State.OK, summary='Status: Success'),
            Result(state=State.OK, summary='Transferred Items: 191.00'),
            Metric('items', 191.0),
            Result(state=State.OK, summary='Transferred Data: 142 B'),
            Metric('transferred', 142.0),
            Result(state=State.OK, summary='Backup duration: 2 minutes 9 seconds'),
            Metric('duration', 128.7511818),
            Result(state=State.WARN, notice='Last Success: 1 hour 0 minutes (warn/crit at 30 minutes 0 seconds/5 days 20 hours)'),
            Metric('age', 3641.0, levels=(1800.0, 504000.0)),
        ]
    ),
    (
        'cmk.onmicrosoft.com Outlook Online', {'jobId': '01234567-89ab-cdef-0123-456789abcdef', 'success_maxage': ('fixed', (1800, 3600))},
        [
            Result(state=State.OK, summary='Status: Success'),
            Result(state=State.OK, summary='Transferred Items: 191.00'),
            Metric('items', 191.0),
            Result(state=State.OK, summary='Transferred Data: 142 B'),
            Metric('transferred', 142.0),
            Result(state=State.OK, summary='Backup duration: 2 minutes 9 seconds'),
            Metric('duration', 128.7511818),
            Result(state=State.CRIT, notice='Last Success: 1 hour 0 minutes (warn/crit at 30 minutes 0 seconds/1 hour 0 minutes)'),
            Metric('age', 3641.0, levels=(1800.0, 3600.0)),
        ]
    ),
    (
        'cmk.onmicrosoft.com Outlook Online3', {'jobId': '23456789-abcd-ef01-2345-6789abcdef01', 'success_maxage': ('fixed', (86400, 504000))},
        [
            Result(state=State.OK, summary='Running since: 5 minutes 14 seconds'),
            Result(state=State.WARN, summary='Last Success: 1 day 1 hour (warn/crit at 1 day 0 hours/5 days 20 hours)'),
            Metric('age', 90041.0, levels=(86400.0, 504000.0)),
        ]
    ),
])
def test_check_veeam_o365jobs(item, params, result):
    fullparams = veeam_o365jobs.VEEAM_O365JOBS_CHECK_DEFAULT_PARAMETERS.copy()
    fullparams.update(params)
    assert list(veeam_o365jobs.check_veeam_o365jobs(item, fullparams, EXAMPLE_SECTION)) == result
