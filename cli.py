#!/usr/bin/python

from r515.projector import Connection, BasicFunctions
import argparse

def lampOn(R515):
    #Turn Lamp on
    R515.send("command/projector/power/set?state=on")

def projectorStandby(prj):
    #Turn Lamp off
    prj.send("command/projector/power/set?state=standby")

def openDouser():
    #Open Douser
    request = Request("https://192.168.3.10/command/projector/shutter/set?state=off", headers={'Cookie':cookie})
    response = urlopen(request)

    print(response.read())	

def closeDouser():
    #Open Douser
    request = Request("https://192.168.3.10/command/projector/shutter/set?state=on", headers={'Cookie':cookie})
    response = urlopen(request)

    print(response.read())

def gong():
    #Drei Gong
    request = Request("https://192.168.3.10/playback/command", headers={'Cookie':cookie}, data='<SMSMessage xmlns="http://xmlns.sony.net/d-cinema/sms/2007a"><MessageHeader><Id>12345</Id><Type>Command</Type><Timestamp>1000</Timestamp><Source>PJT</Source></MessageHeader><MessageBody><Command><Operation>Play</Operation><ParameterList><Parameter><Name>Id</Name><Value>urn:uuid:3cf2c110-6041-436f-9358-8e20e851797e</Value></Parameter><Parameter><Name>Type</Name><Value>CPL</Value></Parameter><Parameter><Name>StartPoint</Name><Value>00:00:00</Value></Parameter></ParameterList></Command></MessageBody></SMSMessage>')
    response = urlopen(request)

    print(response.read())

def changeFormat(id):
    if id in range(0, 65):
        request = Request("https://192.168.3.10/command/projector/function/set?id="+id, headers={'Cookie':cookie})
        response = urlopen(request)
    
        print(response.read())

parser = argparse.ArgumentParser(description='Command line interface for the Sony R515P Server.')
parser.add_argument('--on', action='store_true',
                   help='Turns the projector on, ready for projection.')
parser.add_argument('--standby', action='store_true',
                   help='Turns the projector into Standby.')
parser.add_argument('--open', action='store_true',
                   help='Open Douser.')
parser.add_argument('--close', action='store_true',
                   help='Close Douser.')
parser.add_argument('--gong', action='store_true',
                   help='Play Gong.')
parser.add_argument('--format', nargs=1,
                   help='Change format to id')

args = parser.parse_args()

projector = projector.Connection("192.168.3.10", "filmkreis", "film54")

"""if len(args) == 0:
    #TODO: Hilfe ausgeben!
    pass"""
if args.on:
    lampOn(projector)
elif args.standby:
    projectorStandby(projector)
elif args.open:
    openDouser()
elif args.close:
    closeDouser()
elif args.gong:
    gong()
elif args.format:
    changeFormat(args.format[0]-1)

del projector
