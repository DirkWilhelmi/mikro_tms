#!/usr/bin/python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import re

class Library(object):
    """Eine Klasse die die Library kapselt"""
    def __init__(self, connection):
	    """Erzeugt eine neue Klasse, benötigt ein Verbindungsobjekt"""
	    self._prj = connection
