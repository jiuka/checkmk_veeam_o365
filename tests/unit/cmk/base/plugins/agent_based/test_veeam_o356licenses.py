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
from cmk.base.plugins.agent_based import veeam_o365licenses


@pytest.mark.parametrize('section, result', [
    ([], []),
    (
        [['Valid', '28.06.2020 02:00:00', '2592000', '42', '50000']],
        [Service(item='0')]
    )
])
def test_discovery_veeam_o365licenses(section, result):
    assert list(veeam_o365licenses.discovery_veeam_o365licenses(section)) == result


@pytest.mark.parametrize('item, params, section, result', [
    ('0', {}, [], []),
    (
        '0', {},
        [['Valid', '28.06.2020 02:00:00', '2592000', '42', '50000']],
        [
            Result(state=State.OK, summary='License is vaild till 28.06.2020 02:00:00'),
            Result(state=State.OK, summary='Period of validity: 30 days 0 hours'),
            Metric('licenses', 42.0, levels=(50000.0, 50000.0), boundaries=(0.0, 50000.0)),
            Result(state=State.OK, summary='used 42 out of 50000 licenses (warn/crit at 50000/50000)'),
        ]
    ),
    (
        '0', {'validity': (3456000, 1728000)},
        [['Valid', '28.06.2020 02:00:00', '2592000', '42', '50000']],
        [
            Result(state=State.OK, summary='License is vaild till 28.06.2020 02:00:00'),
            Result(state=State.WARN, summary='Period of validity: 30 days 0 hours (warn/crit below 40 days 0 hours/20 days 0 hours)'),
            Metric('licenses', 42.0, levels=(50000.0, 50000.0), boundaries=(0.0, 50000.0)),
            Result(state=State.OK, summary='used 42 out of 50000 licenses (warn/crit at 50000/50000)'),
        ]
    ),
    (
        '0', {'licenses': (10, 5)},
        [['Valid', '28.06.2020 02:00:00', '2592000', '42', '50']],
        [
            Result(state=State.OK, summary='License is vaild till 28.06.2020 02:00:00'),
            Result(state=State.OK, summary='Period of validity: 30 days 0 hours'),
            Metric('licenses', 42.0, levels=(40.0, 45.0), boundaries=(0.0, 50.0)),
            Result(state=State.WARN, summary='used 42 out of 50 licenses (warn/crit at 40/45)'),
        ]
    ),
    (
        '0', {},
        [['Valid', '28.06.2020 02:00:00', '-2592000', '42', '50']],
        [
            Result(state=State.OK, summary='License is vaild till 28.06.2020 02:00:00'),
            Result(state=State.CRIT, summary='Expired since: 30 days 0 hours (warn/crit below 0 seconds/0 seconds)'),
            Metric('licenses', 42.0, levels=(50.0, 50.0), boundaries=(0.0, 50.0)),
            Result(state=State.OK, summary='used 42 out of 50 licenses (warn/crit at 50/50)'),
        ]
    ),
])
def test_check_veeam_o365licenses(item, params, section, result):
    assert list(veeam_o365licenses.check_veeam_o365licenses(item, params, section)) == result
