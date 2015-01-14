#!/usr/bin/python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import re

class BasicSettings(object):
    """Eine Klasse die die grundlegenden Einstellungen kapselt"""
    def __init__(self, connection):
        """Erzeugt eine neue Klasse, benötigt ein Verbindungsobjekt"""
        self._prj = connection

    def load_format(self, id):
        """Lädt das Bildformat id, possible exceptions: ValueError, RemoteIndexError"""
        try:
            id_intern = int(id)-1
        except ValueError:
            print("ID: "+id+" is not an integer, load_format failed")
            raise ValueError(id)
        if id_intern in range(0, 65):
            self._prj.send("command/projector/function/set?id="+str(id_intern))
        else:
            raise RemoteIndexError(id_intern)

    def save_format(self, id):
        """Saves current settings as id, possible exceptions: ValueError, RemoteIndexError"""
        try:
            id_intern = int(id)-1
        except ValueError:
            print("ID: "+id+" is not an integer, save_format failed")
            raise ValueError(id)
        if id_intern in range(0, 65):
            #TODO
            print("save_format is not yet implemented")
            pass
        else:
            raise RemoteIndexError(id_intern)

    def start_zoom(self, direction = 'up', value = 16777215):
        """Activates the zoom motor"""
        if direction == 'up':
            value = value * -1
        self._prj.send('command/projector/lens/set?target=zoom&direction='+direction+'&value='+str(value))

    def stop_zoom(self, direction = 'up'):
        """Stops the zoom motor"""
        value = "0"        
        if direction == 'up':
            value = "-0"
        self._prj.send('command/projector/lens/set?target=zoom&direction='+direction+'&value='+value)

    def start_focus(self, direction = 'up', value = 16777215):
        """Activates the focus motor"""
        if direction == 'up':
            value = value * -1
        self._prj.send('command/projector/lens/set?target=focus&direction='+direction+'&value='+str(value))

    def stop_focus(self, direction = 'up'):
        """Stops the focus motor"""
        value = "0"        
        if direction == 'up':
            value = "-0"
        self._prj.send('command/projector/lens/set?target=focus&direction='+direction+'&value='+value)

    def set_v_shift(self, value):
        """Set the vertical shift"""
        try:
            value_intern = int(value)
        except ValueError:
            print("Value: "+value+" is not an integer, set_v_shift failed")
            raise ValueError(value)
        if value_intern in range(-511, 512):
            self._prj.send('command/projector/lens/set?target=vshift&value='+str(value_intern))
        else:
            raise RemoteIndexError(value_intern)

    def set_h_shift(self, value):
        """Set the horizontal shift"""
        try:
            value_intern = int(value)
        except ValueError:
            print("Value: "+value+" is not an integer, set_h_shift failed")
            raise ValueError(value)
        if value_intern in range(-511, 512):
            self._prj.send('command/projector/lens/set?target=vshift&value='+str(value_intern))
        else:
            raise RemoteIndexError(value_intern)

    def set_active_lamps(self, value):
        """Set the number of active lamps"""
        try:
            value_intern = int(value)
        except ValueError:
            print("Value: "+value+" is not an integer, set_active_lamps failed")
            raise ValueError(value)
        if value_intern in range(1, 7):
            self._prj.send("config/projector/lamp/lightnumber/set", data='<SMSMessage><MessageHeader><Id>-1</Id><Type>PrjCommand</Type><Timestamp>1400763063474</Timestamp><Source>LSM-100v2</Source></MessageHeader><MessageBody><PrjCommand><ParameterList><Parameter><Name>LightingNumber</Name><Value>'+str(value_intern)+'</Value></Parameter><Parameter><Name>Is3DLens</Name><Value>false</Value></Parameter></ParameterList></PrjCommand></MessageBody></SMSMessage>')
        else:
            raise RemoteIndexError(value_intern)

    def get_active_lamps(self):
        """Get the number of active lamps"""
        #TODO
        pass

    def set_input(self, value):
        """Set the active input"""
        #TODO
        pass

    def get_projector_settings(self):
        """Get some settings"""
        xml = self._prj.send("config/projector/install/settings")
        xml = re.sub(' xmlns="[^"]+"', '', xml, count=1)
        root = ET.fromstring(xml)
        body = root.find('MessageBody')
        settings = body.find('PrjInstallReadableSettings')
        v_shift = settings.find('ElectronicVShift').text
        h_shift = settings.find('MasterHShift').text
        lamp_power = settings.find('LampPower').text
        picture_mode = settings.find('PicutureMode').text
        return {'v_shift': v_shift, 'h_shift': h_shift, 'lamp_power': lamp_power, 'picture_mode': picture_mode}

class RemoteIndexError(Exception):
    """Raised if Index is out of bounds"""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
