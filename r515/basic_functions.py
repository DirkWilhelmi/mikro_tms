#!/usr/bin/python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import re

class BasicFunctions(object):
    """Eine Klasse die die grundlegenden Funktionen kapselt"""
    def __init__(self, connection):
	    """Erzeugt eine neue Klasse, benötigt ein Verbindungsobjekt"""
	    self._prj = connection

    def power_on(self):
        """Projektor anschalten"""
        self._prj.send("command/projector/power/set?state=on")

    def power_standby(self):
        """Projektor in StandBy setzen"""
        self._prj.send("command/projector/power/set?state=standby")

    def open_douser(self):
        """Klappe auf"""
        self._prj.send("command/projector/shutter/set?state=off")

    def close_douser(self):
        """Klappe zu"""
        self._prj.send("command/projector/shutter/set?state=on")

    def play(self, uuid = None, typ = None, offset = None):
        """Spielt eine übergebene CPL/SPL ab, Offset in seconds, typ als String 'CPL' oder 'SPL'"""
        info = None
        if uuid == None:
            info = (self.get_show_info() if info == None else info)
            uuid = info['uuid']
        if typ == None:
            info = (self.get_show_info() if info == None else info)
            typ = info['typ']
        if offset == None:
            info = (self.get_show_info() if info == None else info)
            offset = int(info['time']['elapsed'])/1000
        offset_string = _seconds_to_string(offset)
        self._prj.send("playback/command", '<SMSMessage xmlns="http://xmlns.sony.net/d-cinema/sms/2007a"><MessageHeader><Id>12345</Id><Type>Command</Type><Timestamp>1000</Timestamp><Source>PJT</Source></MessageHeader><MessageBody><Command><Operation>Play</Operation><ParameterList><Parameter><Name>Id</Name><Value>'+uuid+'</Value></Parameter><Parameter><Name>Type</Name><Value>'+typ+'</Value></Parameter><Parameter><Name>StartPoint</Name><Value>'+offset_string+'</Value></Parameter></ParameterList></Command></MessageBody></SMSMessage>')
        print "Send ID", uuid
        #TODO: Catch potential Errors (Other playing operation in progress, etc.)

    def pause(self):
        """Pausiert die Wiedergabe"""
        self._prj.send("playback/command", '<SMSMessage xmlns="http://xmlns.sony.net/d-cinema/sms/2007a"><MessageHeader><Id>12345</Id><Type>Command</Type><Timestamp>1000</Timestamp><Source>PJT</Source></MessageHeader><MessageBody><Command><Operation>Pause</Operation></Command></MessageBody></SMSMessage>')

    def resume(self):
        """Hebt die Pause wieder auf"""
        self._prj.send("playback/command", '<SMSMessage xmlns="http://xmlns.sony.net/d-cinema/sms/2007a"><MessageHeader><Id>12345</Id><Type>Command</Type><Timestamp>1000</Timestamp><Source>PJT</Source></MessageHeader><MessageBody><Command><Operation>Resume</Operation></Command></MessageBody></SMSMessage>')

    def stop(self):
        """Stoppt die Wiedergabe"""
        info = self.get_show_info()
        offset_string = _seconds_to_string(int(info['time']['elapsed'])/1000)
        self._prj.send("playback/command", '<SMSMessage xmlns="http://xmlns.sony.net/d-cinema/sms/2007a"><MessageHeader><Id>12345</Id><Type>Command</Type><Timestamp>1000</Timestamp><Source>PJT</Source></MessageHeader><MessageBody><Command><Operation>Stop</Operation><ParameterList><Parameter><Name>Id</Name><Value>'+info['uuid']+'</Value></Parameter><Parameter><Name>Type</Name><Value>'+info['typ']+'</Value></Parameter><Parameter><Name>StartPoint</Name><Value>'+offset_string+'</Value></Parameter></ParameterList></Command></MessageBody></SMSMessage>')

    def get_show_info(self):
        """Get Info about the current show"""
        xml = self._prj.send("playback/showstatus")
        xml = re.sub(' xmlns="[^"]+"', '', xml, count=1)
        root = ET.fromstring(xml)
        body = root.find('MessageBody')
        body = body.find('ShowStatus')
        status = body.find('PlayState').text
        if status == "NONE":
            return {'uuid': None, 'typ': "CPL", 'status': status, 'time': {'remaining': 0, 'elapsed': 0, 'total': 0}}
        body = body.find('ShowStatusDetail')
        uuid = body.find('Id').text
        c_or_s = body.find('Type').text
        remaining = body.find('RemainingTime').text
        elapsed = body.find('ElapsedTime').text
        total = body.find('TotalDuration').text
        info = {'uuid': uuid, 'typ': c_or_s, 'status': status, 'time': {'remaining': remaining, 'elapsed': elapsed, 'total': total}}
        if c_or_s == "CPL":
            return {'uuid': uuid, 'typ': c_or_s, 'status': status, 'time': {'remaining': remaining, 'elapsed': elapsed, 'total': total}}
        event_uuid = body.find('CurrentEventId').text
        event_type = body.find('CurrentEventType').text
        return {'uuid': uuid, 'typ': c_or_s, 'status': status, 'time': {'remaining': remaining, 'elapsed': elapsed, 'total': total}, 'event_uuid': event_uuid, 'event_type': event_type}

    def get_power_status(self):
        xml = self._prj.send("status/sms/powerstatus")
        xml = re.sub(' xmlns="[^"]+"', '', xml, count=1)
        root = ET.fromstring(xml)
        body = root.find('MessageBody')
        body = body.find('PowerStatusList')
        for status in body.iter('PowerStatus'):
            if status.find('Device').text == 'PRJ':
                return status.find('State').text
        return None

def _seconds_to_string(seconds):
    """Helperfunction to generate the timestrings"""
    offset_stunden = seconds/3600
    offset_minuten = (seconds%3600)/60
    offset_sekunden = seconds%60
    return '%(stunden)02d:%(minuten)02d:%(sekunden)02d' % {"stunden": offset_stunden, "minuten": offset_minuten, "sekunden": offset_sekunden}
