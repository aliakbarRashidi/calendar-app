# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
#
# Copyright (C) 2013, 2014 Canonical Ltd
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

"""Calendar app autopilot tests."""

from __future__ import absolute_import

import logging
import datetime

from autopilot.matchers import Eventually
from testtools.matchers import Equals

from calendar_app import data
from calendar_app.tests import CalendarAppTestCaseWithVcard

logger = logging.getLogger(__name__)


class NewEventTestCase(CalendarAppTestCaseWithVcard):

    # TODO add tests for events in the future and in the past, all day event,
    # event with recurrence and event with reminders.
    # also add tests for saving to different calendars
    # We currently can't change the date of the new event because of bug
    # http://pad.lv/1328600 on Autopilot.
    # --elopio - 2014-06-26

    def _try_delete_event(self, event_name):
        try:
            day_view = self.app.main_view.go_to_day_view()
            day_view.delete_event(event_name)
        except Exception as exception:
            logger.warn(str(exception))

    def _add_event(self):
        test_event = data.Event.make_unique()
        new_event_page = self.app.main_view.go_to_new_event()
        new_event_page.add_event(test_event)

        self.assertThat(lambda: self._event_exists(test_event.name),
                        Eventually(Equals(True)))

        return test_event

    def _edit_event(self, event_name):
        test_event = data.Event.make_unique()
        day_view = self.app.main_view.go_to_day_view()

        new_event_page = day_view.edit_event(event_name)

        new_event_page.add_event(test_event)
        return test_event

    def _event_exists(self, event_name):
        try:
            day_view = self.app.main_view.go_to_day_view()
            day_view.get_event(event_name, True)
        except Exception:
            return False
        return True

    def _expected_start_date(self):
        now = datetime.datetime.now()
        now = datetime.datetime(now.year, now.month,
                                now.day, now.hour, now.minute)

        if now.minute < 30:
            return datetime.datetime(now.year, now.month,
                                     now.day, now.hour, 30)
        else:
            start_date = datetime.datetime(now.year, now.month,
                                           now.day, now.hour, 0)
            return start_date + datetime.timedelta(hours=1)

    def test_new_event_must_start_with_default_values(self):
        """Test adding a new event default values

           Start Date: today Start Time: next half hour increment
           End Date: today End Time: 1 hour after start time
           Calendar: Personal
           All Day Event: unchecked
           Event Name: blank, selected
           Description: blank
           Location: none
           Guests: none
           This happens: Once
           Remind me: On Event
        """

        new_event_page = self.app.main_view.go_to_new_event()
        self.assertThat(new_event_page.get_calendar_name(), Equals('Personal'))
        self.assertThat(new_event_page.get_event_name(), Equals(''))
        self.assertThat(new_event_page.get_description_text(), Equals(''))
        self.assertThat(new_event_page.get_location_name(), Equals(''))
        self.assertThat(new_event_page.get_is_all_day_event(), Equals(False))
        self.assertThat(new_event_page.has_guests(), Equals(False))
        self.assertThat(new_event_page.get_this_happens(), Equals('Once'))
        self.assertThat(new_event_page.get_reminder(), Equals('On Event'))

        expected_start_date = self._expected_start_date()
        expected_end_date = expected_start_date + datetime.timedelta(hours=1)

        self.assertThat(new_event_page.get_start_date(),
                        Equals(expected_start_date))
        self.assertThat(new_event_page.get_end_date(),
                        Equals(expected_end_date))

    def test_add_new_event_with_default_values(self):
        """Test adding a new event with the default values.

        The event must be created on the currently selected date,
        with an end time, without recurrence and without reminders."""

        test_event = self._add_event()

        self.addCleanup(self._try_delete_event, test_event.name)

        day_view = self.app.main_view.go_to_day_view()
        event_details_page = day_view.open_event(test_event.name)

        self.assertEqual(test_event,
                         event_details_page.get_event_information())

    def test_delete_event_must_remove_it_from_day_view(self):
        """Test deleting an event must no longer show it on the day view."""
        test_event = self._add_event()

        day_view = self.app.main_view.go_to_day_view()
        day_view.delete_event(test_event.name)

        self.assertThat(lambda: self._event_exists(test_event.name),
                        Eventually(Equals(False)))

    def test_edit_event_with_default_values(self):
        """Test editing an event change unique values of an event."""

        original_event = self._add_event()
        edited_event = self._edit_event(original_event.name)
        self.addCleanup(self._try_delete_event, edited_event.name)

        day_view = self.app.main_view.get_day_view()
        event_details_page = day_view.open_event(edited_event.name)

        self.assertEqual(edited_event,
                         event_details_page.get_event_information())
