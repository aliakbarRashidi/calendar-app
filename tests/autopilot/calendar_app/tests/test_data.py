# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
#
# Copyright (C) 2014 Canonical Ltd
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import testtools

from calendar_app import data


class EventTestCase(testtools.TestCase):

    def test_make_unique_event_must_return_event_with_unique_id(self):
        event = data.Event.make_unique(unique_id='test uuid')

        self.assertEqual(event.name, 'Test event test uuid')
        self.assertEqual(event.description, 'Test description test uuid.')
        self.assertEqual(event.location, 'Test location test uuid')
        self.assertEqual(event.guests, 'Test guests test uuid')
