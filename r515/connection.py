#!/usr/bin/python
# -*- coding: utf-8 -*-

from urllib2 import urlopen, Request
import xml.etree.ElementTree as ET
from datetime import datetime
import re

class Connection(object):
    """Eine Verbindungsklasse zum Projektor R515. Besteht aus der Verbindungsinitialisierung, einer send-Funktion sowie einem Destruktor (Logout)"""
    def __init__(self, ip, user, pwd):
        """Erzeugt eine neue R515 Klasse, benötigt die ip, den Nutzernamen und das Password"""
        #debugging?
        self._debug = True
        self._ip = ip
        #get Cookie
        response = urlopen("https://"+ip+"/config/role/list")
        self._cookie = response.info()['Set-Cookie']
        #Login
        self.send("login", "<SMSMessage><MessageHeader><Id>-1</Id><Type>SMSUserSession</Type><Timestamp>0</Timestamp><Source>Theater-0</Source></MessageHeader><MessageBody><SMSUserSession><User>"+user+"</User><Password>"+pwd+"</Password></SMSUserSession></MessageBody></SMSMessage>")

    def send(self, path, data = None):
        """Die Kommando-Send Funktion, gibt die Rückgabe des Servers zurück. Falls Daten übergeben werden => POST, ansonsten GET"""
        if data:
            request = Request("https://"+self._ip+"/"+path, headers={'Cookie':self._cookie}, data=data)
        else:
            request = Request("https://"+self._ip+"/"+path, headers={'Cookie':self._cookie})
        response = urlopen(request)
        response = response.read()
        if self._debug:
            print(response)
        return response

    def get_time_offset(self):
        xml = self.send("show/schedule/mode/get")
        local = datetime.now()
        xml = re.sub(' xmlns="[^"]+"', '', xml, count=1)
        root = ET.fromstring(xml)
        body = root.find('MessageHeader')
        timestamp = int(body.find('Timestamp').text)
        timestamp = datetime.fromtimestamp(timestamp/1000)
        return local - timestamp

    def __del__(self):
        self.send("logout")
