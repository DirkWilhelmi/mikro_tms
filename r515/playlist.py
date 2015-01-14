#!/usr/bin/python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import re

class Playlist(object):
    """SPL-Wrapper Class. Load/Create SPL, Add/Remove CPL, Cue's, Black"""

    def __init__(self, connection, uuid = None):
        """Load/Create SPL"""
        self._prj = connection
        if uuid == None:
            self._spl = ET.parse("spl.xml")
            self._spl = self._spl.getroot()
        else:
            self._spl = ET.fromstring(re.sub(' xmlns="[^"]+"', '', self._prj.send('show/playlist/details/info?Id='+uuid), count=1))
        self._content = self._spl.find("Content")

    def get_event_list(self):
        """Gets a list of events"""
        event_list = []
        for event in self._content:
            if event.tag == "CommandEvent":
                event_list.append({"typ": "CMD", "offset": self._tc_to_ms(event.find('Offset').text), "duration": self._tc_to_ms(event.find('Duration').text), "cmd": {"target": event.find('Target').text, "command": event.find('Command').text, "parameter": event.find('Parameter').attrib}})
            elif event.tag == "CPLEvent":
                event_list.append({"typ": "CPL", "offset": self._tc_to_ms(event.find('Offset').text), "duration": self._tc_to_ms(event.find('Duration').text), "uuid": event.find('Id').text})
            elif event.tag == "SPLEvent":
                event_list.append({"typ": "SPL", "offset": self._tc_to_ms(event.find('Offset').text), "duration": self._tc_to_ms(event.find('Duration').text), "uuid": event.find('Id').text})
    
    def add_cpl(self, uuid):
        """Adds a cpl to the spl"""
        CPLEvent = ET.SubElement(self._content, "CPLEvent")
        ET.SubElement(CPLEvent, "Id").text = uuid
        pass

    def remove_cpl(self, uuid):
        """Removes a cpl from the spl"""
        #TODO
        pass

    def add_spl(self, uuid):
        """Adds a spl to the spl"""
        #TODO
        pass

    def remove_spl(self, uuid):
        """Removes a spl from the spl"""
        #TODO
        pass

    def add_cue(self, offset, command, target, parameter_name, parameter_value):
        """Adds a Automation Cue to the spl"""
        #TODO
        pass

    def remove_cue(self, number):
        """Removes an automation cue from the spl"""
        #TODO
        pass

    def add_black(self, duration):
        """Adds black (Offset)"""
        #TODO
        pass

    def move_element(self, uuid):
        """Moves CPL/SPL"""
        #TODO
        pass

    def change_cue(self, offset = None, command = None, target = None, parameter_name = None, parameter_value = None):
        """Changes Cue"""
        #TODO
        pass
        
    def get_cpl_at_offset(self, offset, accu_offset = 0):
        """Gets the element at offset (in ms)"""
        offset = int(offset)
        for event in self._content.iter("CPLEvent"):
            event_offset = self._tc_to_ms(event.find('Offset').text)
            if offset >= event_offset:
                duration = self._tc_to_ms(event.find('Duration').text)
                event_end = event_offset + duration
                if offset < event_end:
                    return {'uuid': event.find('Id').text, 'type': "CPL", 'offset': event_offset + accu_offset, 'duration': duration}
        for event in self._content.iter("SPLEvent"):
            event_offset = self._tc_to_ms(event.find('Offset').text)
            if offset >= event_offset:
                event_end = self._tc_to_ms(event.find('Duration').text)
                event_end = event_offset + event_end
                if offset < event_end:
                    return Playlist(self._prj, event.find('Id').text).get_cpl_at_offset(offset - event_offset, accu_offset + event_offset)
        return None

    def get_title(self):
        """Returns the SPL's title"""
        return self._spl.find('Metadata').find('Title').text
    
    def _tc_to_ms(self, tc):
        ms = tc.split('.')
        tc = ms[0].split(':')
        ms = ms[1]
        ms = (int(tc[0])*60*60*1000)+(int(tc[1])*60*1000)+(int(tc[2])*1000)+int(ms)
        return ms
