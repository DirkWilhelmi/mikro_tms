#!/usr/bin/python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import re
from playlist import Playlist

class Library(object):
    """Eine Klasse die die Library kapselt"""
    def __init__(self, connection):
	    """Erzeugt eine neue Klasse, benötigt ein Verbindungsobjekt"""
	    self._prj = connection

    def get_cpl_info(self, uuid = None, body = None):
        """Get Info about a cpl"""
        if body == None:
            xml = self._prj.send("content/cpl/info?Id=" + uuid)
            xml = re.sub(' xmlns="[^"]+"', '', xml, count=1)
            root = ET.fromstring(xml)
            body = root.find('MessageBody')
            body = body.find('CPLDetails')
        title = body.find('ContentTitle').text
        typ = body.find('ContentType').text
        language = body.find('SpokenLanguage').text
        subtitle = body.find('SubtitleLanguage').text
        fps = body.find('FrameRate').find('Numerator').text
        ar = ("CS" if body.find('AspectRatio').find('Height').text == "858" or body.find('AspectRatio').find('Height').text == "1716" else "Flat")
        audio_channels = body.find('NumberOfChannels').text
        runtime = body.find('RunningTime').text
        uuid = body.find('ID').text
        return {'uuid': uuid, 'title': title, 'type': typ, 'language': language, 'subtitle': subtitle, 'fps': fps, 'ar': ar, 'audio_channels': audio_channels, 'runtime': runtime}

    def get_cpl_list(self):
        cpl_list = []
        xml = self._prj.send("content/cpl/info/list?detailed=true")
        xml = re.sub(' xmlns="[^"]+"', '', xml, count=1)
        root = ET.fromstring(xml)
        body = root.find('MessageBody')
        body = body.find('CPLDetailsList')
        for cpl in body.iter('CPLDetails'):
            cpl_list.append(self.get_cpl_info(body = cpl))
        return cpl_list
    
    def get_spl_list(self):
        spl_list = []
        xml = self._prj.send("show/playlist/info/list?extended=true")
        xml = re.sub(' xmlns="[^"]+"', '', xml, count=1)
        root = ET.fromstring(xml)
        body = root.find('MessageBody')
        body = body.find('SPLMetadataList')
        for spl in body.iter('SPLMetadata'):
            spl_list.append({'uuid': spl.find('UUID').text, 'title': spl.find('Title').text})
        return spl_list
