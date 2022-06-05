""".. versionadded:: 0.0.1

Control the macOS Calendar application using JXA-like syntax.
"""

from datetime import datetime, timedelta, date
from tracemalloc import start
from typing import List, Literal, Union

from ScriptingBridge import SBObject

from pprint import pprint
import EventKit
import sys
import os

from Foundation import NSURL
from AppKit import NSPredicate, NSMutableArray
from numpy import isin

from PyXA import XABase
from PyXA import XABaseScriptable

# Calendar Constants
_YES = Literal[2036691744]
_NO = Literal[2036691744]
_ASK = Literal[1634954016]
_STANDARD_ERRORS = Literal[1819767668]
_DETAILED_ERRORS = Literal[1819763828]
_PARTICIPATION_UNKNOWN = Literal[1161195105]
_PARTICIPATION_ACCEPTED = Literal[1161191792]
_PARTICIPATION_DECLINED = Literal[1161192560]
_PARTICIPATION_TENTATIVE = Literal[1161196656]
_STATUS_CANCELLED = Literal[1161061217]
_STATUS_CONFIRMED = Literal[1161061230]
_STATUS_NONE = Literal[1161064047]
_STATUS_TENTATIVE = Literal[1161065573]
_NO_PRIORITY = Literal[1952739376]
_LOW_PRIORITY = Literal[1952739385]
_MEDIUM_PRIORITY = Literal[1952739381]
_HIGH_PRIORITY = Literal[1952739377]
_DAY_VIEW = Literal[1161127009]
_WEEK_VIEW = Literal[1161131877]
_MONTH_VIEW = Literal[1161129327]


class XACalendarApplication(XABaseScriptable.XASBApplication, XABase.XACanConstructElement, XABase.XAAcceptsPushedElements, XABase.XACanOpenPath):
    """A class for managing and interacting with scripting elements of the macOS Calendar application.

    .. seealso:: Classes :class:`XACalendar`, :class:`XACalendarEvent`

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_wcls = XACalendarWindow

        # Silence the message EventStore prints to stderr when initializing.
        # from: https://stackoverflow.com/a/3946828
        old_stderr = os.dup(sys.stderr.fileno())
        fd = os.open('/dev/null', os.O_CREAT | os.O_WRONLY)
        os.dup2(fd, sys.stderr.fileno())
        self.xa_estr = EventKit.EKEventStore.alloc().init()
        os.dup2(old_stderr, sys.stderr.fileno())

    def reload_calendars(self) -> 'XACalendarApplication':
        """Reloads the contents of all calendars.

        :return: A reference to the Calendar application object.
        :rtype: XACalendarApplication

        .. versionadded:: 0.0.1
        """
        self.xa_scel.reloadCalendars()
        return self

    def switch_view_to(self, view: Literal["day", "week", "month"]) -> 'XACalendarApplication':
        """Switches to the target calendar view.

        :param view: The view to switch to.
        :type view: Literal["day", "week", "month"]
        :return: A reference to the Calendar application object.
        :rtype: XACalendarApplication

        .. versionadded:: 0.0.1
        """
        view_ids = {
            "day": _DAY_VIEW,
            "week": _WEEK_VIEW,
            "month": _MONTH_VIEW,
        }
        self.xa_scel.switchViewTo_(view_ids[view])
        return self

    def view_calendar_at(self, date: datetime) -> 'XACalendarApplication':
        """Displays the calendar at the provided date.

        :param date: The date to display.
        :type date: datetime
        :return: A reference to the Calendar application object.
        :rtype: XACalendarApplication

        .. versionadded:: 0.0.1
        """
        self.xa_scel.viewCalendarAt_(date)
        return self

    def subscribe_to(self, url: str) -> 'XACalendarApplication':
        """Subscribes to the calendar at the specified URL.

        :param url: The URL of the calendar (in iCal format) to subscribe to.
        :type url: str
        :return: A reference to the Calendar application object.
        :rtype: XACalendarApplication
        """
        self.xa_scel.GetURL_(url)
        return self

    def __new_calendar(self, calender_obj) -> 'XACalendar':
        predicate = NSPredicate.predicateWithFormat_(XABase.xa_predicate_format({"name": calender_obj.title()}))
        scriptable_calendars = self.xa_scel.calendars()
        scriptable_calendar = scriptable_calendars.filteredArrayUsingPredicate_(predicate)[0]
        properties = {
            "parent": self,
            "appspace": self.xa_apsp,
            "workspace": self.xa_wksp,
            "element": calender_obj,
            "scriptable_element": scriptable_calendar,
            "appref": self.xa_aref,
            "system_events": self.xa_sevt,
            "event_store": self.xa_estr,
        }
        return XACalendar(properties)

    def calendars(self, filter: dict = None) -> List['XACalendar']:
        """Returns a list of calendars, as PyXA objects, matching the given filter.

        .. seealso:: :func:`calendar`

        .. versionadded:: 0.0.1
        """
        calendars = self.xa_estr.calendarsForEntityType_(0)
        if filter is not None:
            predicate = NSPredicate.predicateWithFormat_(XABase.xa_predicate_format(filter))
            calendars = calendars.filteredArrayUsingPredicate_(predicate)

        elements = []
        for calendar in calendars:
            elements.append(self.__new_calendar(calendar))
        return elements

    def calendar(self, filter: Union[int, dict]) -> 'XACalendar':
        """Returns the first calendar matching the given filter.

        .. seealso:: :func:`calendars`

        .. versionadded:: 0.0.1
        """
        calendar = None
        calendars = self.xa_estr.calendarsForEntityType_(0)
        if isinstance(filter, int):
            calendar = calendars[filter]
        else:
            predicate = NSPredicate.predicateWithFormat_(XABase.xa_predicate_format(filter))
            calendar = calendars.filteredArrayUsingPredicate_(predicate)[0]
        return self.__new_calendar(calendar)

    def first_calendar(self) -> 'XACalendar':
        """Returns the calendar at the zero index of the calendars array.

        .. versionadded:: 0.0.1
        """
        calendar = self.xa_estr.calendarsForEntityType_(0)[0]
        return self.__new_calendar(calendar)

    def last_calendar(self) -> 'XACalendar':
        """Returns the calendar at the last (-1) index of the calendars array.

        .. versionadded:: 0.0.1
        """
        calendar = self.xa_estr.calendarsForEntityType_(0)[-1]
        return self.__new_calendar(calendar)

    def default_calendar(self) -> 'XACalendar':
        """Returns the calendar that events are added to by default.

        .. versionadded:: 0.0.1
        """
        calendar = self.xa_estr.defaultCalendarForNewEvents()
        return self.__new_calendar(calendar)

    def new_calendar(self, name: str = "New Calendar") -> 'XACalendar':
        """Creates a new calendar with the given name.

        :param name: The name of the calendar, defaults to "New Calendar"
        :type name: str, optional
        :return: A reference to the newly created calendar.
        :rtype: XACalendar

        :Example:

        >>> import PyXA
        >>> app = PyXA.application("Calendar")
        >>> new_cal = app.new_calendar("Work")
        >>> print(new_cal.element.name())
        Work

        .. seealso:: :class:`XACalendar`

        .. versionadded:: 0.0.1
        """
        return self.push("calendar", {"name": name}, self.xa_scel.calendars(), XACalendar)

    def new_event(self, name: str, start_date: datetime, end_date: datetime, calendar: Union['XACalendar', None] = None) -> 'XACalendarEvent':
        """Creates a new event with the given name and start/end dates in the specified calendar. If no calendar is specified, the default calendar is used.

        :param name: The name of the event
        :type name: str
        :param start_date: The start date and time of the event.
        :type start_date: datetime
        :param end_date: The end date and time of the event.
        :type end_date: datetime
        :return: A reference to the newly created event.
        :rtype: XACalendarEvent

        :Example:

        >>> from datetime import datetime, timedelta
        >>> import PyXA
        >>> app = PyXA.application("Calendar")
        >>> start_date = datetime.now()
        >>> end_date = start_date + timedelta(hours = 1)
        >>> new_event = app.new_event("Learn about PyXA", start_date, end_date)
        >>> print(new_event)
        <apps.Calendar.XACalendarEvent object at 0x104d042e0>

        .. seealso:: :class:`XACalendarEvent`

        .. versionadded:: 0.0.1
        """
        if calendar is None:
            return self.push("event", {"summary": name, "startDate": start_date, "endDate": end_date}, self.default_calendar().xa_elem.events(), XACalendarEvent)
        return self.push("event", {"summary": name, "startDate": start_date, "endDate": end_date}, calendar.xa_elem.events(), XACalendarEvent)


class XACalendarWindow(XABase.XAWindow):
    """A class for interacting with windows of Calendar.app.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)

class XACalendar(XABase.XAHasElements, XABase.XAAcceptsPushedElements, XABaseScriptable.XASBPrintable):
    """A class for interacting with calendars.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_estr = properties["event_store"]

        self.title = self.xa_elem.title()
        self.summary = self.xa_elem.summary()
        self.subscription_url = self.xa_elem.subscriptionURL()
        self.sharing_status = self.xa_elem.sharingStatus()
        self.color = self.xa_elem.colorString()
        self.type = self.xa_elem.typeString()
        self.notes = self.xa_elem.notes()
        self.description = self.xa_elem.description()
        self.sharees = self.xa_elem.sharees()

    def __new_event(self, event_obj) -> 'XACalendarEvent':
        predicate = NSPredicate.predicateWithFormat_(XABase.xa_predicate_format({"uid": event_obj.localUID()}))
        scriptable_events = self.xa_scel.events()
        scripable_event = scriptable_events.filteredArrayUsingPredicate_(predicate)[0]
        properties = {
            "parent": self,
            "appspace": self.xa_apsp,
            "workspace": self.xa_wksp,
            "element": event_obj,
            "scriptable_element": scripable_event,
            "appref": self.xa_aref,
            "system_events": self.xa_sevt,
            "event_store": self.xa_estr,
        }
        return XACalendarEvent(properties)

    def events(self, filter: dict = None) -> List['XACalendarEvent']:
        """Returns a list of events, as PyXA objects, matching the given filter.

        .. seealso:: :func:`event`

        .. versionadded:: 0.0.1
        """
        calendar = self.xa_elem
        events = NSMutableArray.arrayWithArray_([])
        for year in range(2006, datetime.now().year + 4, 4):
            start_date = date(year, 1, 1)
            end_date = start_date + timedelta(days = 365 * 4)
            predicate = self.xa_estr.predicateForEventsWithStartDate_endDate_calendars_(start_date, end_date, [calendar])
            events.addObjectsFromArray_(self.xa_estr.eventsMatchingPredicate_(predicate))

        if filter is not None:
            predicate = NSPredicate.predicateWithFormat_(XABase.xa_predicate_format(filter))
            events = events.filteredArrayUsingPredicate_(predicate)

        elements = []
        for event in events:
            elements.append(self.__new_event(event))
        return elements

    def events_today(self) -> List['XACalendarEvent']:
        """Gets a list of all events in the next 24 hours.

        :return: The list of events.
        :rtype: List['XACalendarEvent']

        .. seealso:: :func:`week_events`

        .. versionadded:: 0.0.1
        """
        start_date = datetime.now()
        end_date = start_date + timedelta(days = 1)
        return self.events_in_range(start_date, end_date)

    def week_events(self) -> List['XACalendarEvent']:
        """Gets a list of events occurring in the next 7 days.

        :return: The list of events.
        :rtype: List['XACalendarEvent']

        .. seealso:: :func:`events_today`

        .. versionadded:: 0.0.1
        """
        start_date = datetime.now()
        end_date = start_date + timedelta(days = 7)
        return self.events_in_range(start_date, end_date)

    def events_in_range(self, start_date: datetime, end_date: datetime) -> List['XACalendarEvent']:
        """Gets a list of events occurring between the specified start and end datetimes.

        :param start_date: The earliest date an event in the list should begin.
        :type start_date: datetime
        :param end_date: The latest date an event in the list should end.
        :type end_date: datetime
        :return: The list of events.
        :rtype: List['XACalendarEvent']

        .. versionadded:: 0.0.1
        """
        calendar = self.xa_elem
        predicate = self.xa_estr.predicateForEventsWithStartDate_endDate_calendars_(start_date, end_date, [calendar])
        events = self.xa_estr.eventsMatchingPredicate_(predicate)

        elements = []
        for event in events:
            elements.append(self.__new_event(event))
        return elements

    def event(self, filter: Union[int, dict]) -> 'XACalendarEvent':
        """Returns the first event matching the given filter.

        .. seealso:: :func:`events`

        .. versionadded:: 0.0.1
        """
        calendar = self.xa_elem
        events = NSMutableArray.arrayWithArray_([])
        for year in range(2006, datetime.now().year + 4, 4):
            start_date = date(year, 1, 1)
            end_date = start_date + timedelta(days = 365 * 4)
            predicate = self.xa_estr.predicateForEventsWithStartDate_endDate_calendars_(start_date, end_date, [calendar])
            events.addObjectsFromArray_(self.xa_estr.eventsMatchingPredicate_(predicate))
        
        event = None
        if isinstance(filter, int):
            event = events[filter]
        else:
            predicate = NSPredicate.predicateWithFormat_(XABase.xa_predicate_format(filter))
            event = events.filteredArrayUsingPredicate_(predicate)[0]
        return self.__new_event(event)
        
    def first_event(self) -> 'XACalendarEvent':
        """Returns the event at the zero index of the events array.

        .. versionadded:: 0.0.1
        """
        calendar = self.xa_elem
        events = NSMutableArray.arrayWithArray_([])
        for year in range(2006, datetime.now().year + 4, 4):
            start_date = date(year, 1, 1)
            end_date = start_date + timedelta(days = 365 * 4)
            predicate = self.xa_estr.predicateForEventsWithStartDate_endDate_calendars_(start_date, end_date, [calendar])
            events.addObjectsFromArray_(self.xa_estr.eventsMatchingPredicate_(predicate))
            if len(events) > 0:
                break
        return self.__new_event(events[0])

    def last_event(self) -> 'XACalendarEvent':
        """Returns the event at the last (-1) index of the events array.

        .. versionadded:: 0.0.1
        """
        calendar = self.xa_elem
        events = NSMutableArray.arrayWithArray_([])
        for year in range(datetime.now().year, 2002, -4):
            start_date = date(year, 1, 1)
            end_date = start_date + timedelta(days = 365 * 4)
            predicate = self.xa_estr.predicateForEventsWithStartDate_endDate_calendars_(start_date, end_date, [calendar])
            events.addObjectsFromArray_(self.xa_estr.eventsMatchingPredicate_(predicate))
            if len(events) > 0:
                break
        return self.__new_event(events[0])

    def push(self, element: SBObject) -> 'XACalendarEvent':
        """Push a new element onto this calendar's list of events.

        :param element_specifier: An element created via this object's :func:`construct` method.
        :type element_specifier: SBObject
        :return: A reference to the newly created event.
        :rtype: XACalendarEvent

        :Example:

        >>> from datetime import datetime, timedelta
        >>> import PyXA
        >>> app = PyXA.application("Calendar")
        >>> start_date = datetime.now()
        >>> end_date = start_date + timedelta(hours = 1)
        >>> new_event = app.construct("event", {"summary": "Learn about PyXA", "startDate": start_date, "endDate": end_date})
        >>> print(cal.push(new_event))
        <apps.Calendar.XACalendarEvent object at 0x104d042e0>

        .. seealso:: :func:`new_event`, :func:`construct`

        .. versionadded:: 0.0.1
        """
        return super().push(element, None, self.xa_elem.events(), XACalendarEvent)

    def new_event(self, name: str, start_date: datetime, end_date: datetime) -> 'XACalendarEvent':
        """Create a new event and push it onto this calendar's events array.

        :param name: The name of the event.
        :type name: str
        :param start_date: The start date and time of the event.
        :type start_date: datetime
        :param end_date: The end date and time of the event.
        :type end_date: datetime
        :return: A reference to the newly created event.
        :rtype: XACalendarEvent

        :Example:

        >>> from datetime import datetime, timedelta
        >>> import PyXA
        >>> app = PyXA.application("Calendar")
        >>> start_date = datetime.now()
        >>> end_date = start_date + timedelta(hours = 1)
        >>> new_event = app.new_event("Learn about PyXA", start_date, end_date)
        >>> print(new_event)
        <apps.Calendar.XACalendarEvent object at 0x104d042e0>

        .. seealso:: :func:`push`, :func:`construct`

        .. versionadded:: 0.0.1
        """
        return self.xa_prnt.new_event(name, start_date, end_date, self)

    def __repr__(self):
        return self.xa_elem.title()


class XACalendarEvent(XABase.XAObject):
    """A class for interacting with calendar events.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.xa_estr = properties["event_store"]
        
        self.description = self.xa_elem.description()
        self.creation_date = self.xa_elem.creationDate()
        self.start_date = self.xa_elem.startDate()
        self.end_date = self.xa_elem.endDate()
        self.all_day_event = self.xa_elem.allDay() == 1
        self.recurrence = self.xa_elem.recurrenceRuleString()
        self.sequence = self.xa_elem.sequence()
        self.stamp_date = self.xa_elem.lastModifiedDate()
        self.status = self.xa_elem.status()
        self.title = self.xa_elem.title()
        self.location = self.xa_elem.location()
        self.travel_duration = self.xa_elem.travelDuration()
        self.duration = self.xa_elem.duration()
        self.uid = self.xa_elem.localUID()
        self.identifier = self.xa_elem.calendarItemIdentifier()
        self.url = self.xa_elem.URL()
        self.notes = self.xa_elem.notes()
        self.organizer_name = self.xa_elem.organizerName()
        self.organizer_email = self.xa_elem.organizerEmail()
        self.organizer_phone_number = self.xa_elem.organizerPhoneNumber()
        self.availability = self.xa_elem.availability()

    def rename(self, new_title: str) -> 'XACalendarEvent':
        """Renames the event.

        :param new_title: The new title of the event
        :type new_title: str
        :return: A reference to the event object.
        :rtype: XACalendarEvent

        .. versionadded:: 0.0.1
        """
        self.xa_scel.setValue_forKey_(new_title, "summary")
        return self

    def delete(self):
        """Deletes the event.

        .. versionadded:: 0.0.1
        """
        self.xa_elem.markAsDeleted()
        self.xa_estr.removeEvent_span_error_(self.xa_elem, EventKit.EKSpanThisEvent, None)

    def duplicate(self) -> 'XACalendarEvent':
        """Duplicates the event, placing the copy on the same calendar.

        :return: A reference to this event object.
        :rtype: XACalendarEvent

        .. versionadded:: 0.0.1
        """
        new_event = self.xa_elem.duplicate()
        self.xa_estr.saveEvent_span_error_(new_event, EventKit.EKSpanThisEvent, None)

    def copy_to(self, calendar: XACalendar) -> 'XACalendarEvent':
        """Makes a copy of this event and places it on the specified calendar.

        :param calendar: The calendar to copy the event to.
        :type calendar: XACalendar
        :return: A reference to this event object.
        :rtype: XACalendarEvent

        .. versionadded:: 0.0.1
        """
        self.xa_elem.copyToCalendar_withOptions_(calendar.xa_elem, 1)
        self.xa_estr.saveCalendar_commit_error_(calendar.xa_elem, True, None)
        return self

    def move_to(self, calendar: XACalendar) -> 'XACalendarEvent':
        """Moves this event to the specified calendar.

        :param calendar: The calendar to move the event to.
        :type calendar: XACalendar
        :return: A reference to this event object.
        :rtype: XACalendarEvent

        .. versionadded:: 0.0.1
        """
        self.copy_to(calendar)
        self.delete()
        return self

    def add_attachment(self, path: Union[str, NSURL]) -> 'XACalendarEvent':
        """Adds the file at the specified path as an attachment to the event.

        :param path: The path of the file to attach to the event.
        :type path: Union[str, NSURL]
        :return: A reference to this event object.
        :rtype: XACalendarEvent

        .. versionadded:: 0.0.1
        """
        if isinstance(path, str):
            url = NSURL.alloc().initFileURLWithPath_(path)
        attachment = EventKit.EKAttachment.alloc().initWithFilepath_(url)
        self.xa_elem.addAttachment_(attachment)
        self.xa_estr.saveEvent_span_error_(self.xa_elem, EventKit.EKSpanThisEvent, None)
        return self

    def show(self) -> 'XACalendarEvent':
        """Shows the event in a calendar window.

        :return: A reference to the event object.
        :rtype: XACalendarEvent

        .. versionadded:: 0.0.1
        """
        self.xa_scel.show()

    # Attachments
    def __new_attachment(self, attachment_obj: EventKit.EKAttachment) -> 'XACalendarAttachment':
        """Wrapper for creating a new PyXA attachment object.

        :param attachment_obj: The EKAttachment object to wrap
        :type attachment_obj: EKAttachment
        :return: The PyXA object representation of the attachment
        :rtype: XACalendarAttachment

        .. versionadded:: 0.0.1
        """
        properties = {
            "parent": self,
            "appspace": self.xa_apsp,
            "workspace": self.xa_wksp,
            "element": attachment_obj,
            "appref": self.xa_aref,
            "system_events": self.xa_sevt,
        }
        return XACalendarAttachment(properties)

    def attachments(self, filter: dict = None) -> List['XACalendarEvent']:
        """Returns a list of attachments, as PyXA objects, matching the given filter.

        .. versionadded:: 0.0.1
        """
        attachments = self.xa_elem.attachments()
        if len(attachments) == 0:
            return []

        if filter is not None:
            predicate = NSPredicate.predicateWithFormat_(XABase.xa_predicate_format(filter))
            attachments = attachments.filteredArrayUsingPredicate_(predicate)

        elements = []
        for attachment in attachments:
            elements.append(self.__new_attachment(attachment))
        return elements

    def display_alarms():
        pass

    def mail_alarms():
        pass

    def open_file_alarms():
        pass

    def sound_alarms():
        pass

    def attendees(self):
        print(self.xa_elem.attendees()[0].comment())
        return

class XACalendarAttachment(XABase.XAObject):
    """A class for interacting with calendar event attachments.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.type = self.xa_elem.contentType()
        self.filename = self.xa_elem.filenameSuggestedByServer()
        self.file = self.xa_elem.urlOnDisk()
        self.url = self.xa_elem.urlOnServer()
        self.uuid = self.xa_elem.uuid()

class XACalendarAttendee(XABase.XAObject):
    """A class for interacting with calendar event attendees.

    .. versionadded:: 0.0.1
    """
    def __init__(self, properties):
        super().__init__(properties)
        self.name = self.xa_elem.name()
        self.first_name = self.xa_elem.firstName()
        self.last_name = self.xa_elem.lastName()
        self.email_address = self.xa_elem.emailAddress()
        self.phone_number = self.xa_elem.phoneNumber()
        self.invited_by = self.xa_elem.inviterNameString()