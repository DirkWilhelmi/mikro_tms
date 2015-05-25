import ConfigParser
from r515.basic_functions import BasicFunctions
from r515.basic_settings import BasicSettings
from r515.connection import Connection

config = ConfigParser.ConfigParser()
config.read(['r515.cfg'])

conn = Connection(config.get('Connection', 'IP'), config.get('Connection', 'USR'), config.get('Connection', 'PWD'))
prj = BasicFunctions(conn)
settings = BasicSettings(conn)


def lamp_on():
    prj.power_on()


def lamp_off():
    prj.power_standby()


def lamp_eighty():
    settings.set_lamp_power(80.0)


def lamp_hundred():
    settings.set_lamp_power(100.0)


def stop():
    prj.stop()
    prj.close_douser()


def pause():
    prj.pause()


def play():
    prj.play()


def dci_flat():
    settings.load_format(1)


def dci_cs():
    settings.load_format(2)


def hdmi_flat():
    settings.load_format(3)


def hdmi_cs():
    settings.load_format(4)


def dowser_close():
    prj.close_douser()


def dowser_open():
    prj.open_douser()


def start_zoom_positive():
    settings.start_zoom()


def stop_zoom_positive():
    settings.stop_zoom()


def start_zoom_down():
    settings.start_zoom('down')


def stop_zoom_down():
    settings.stop_zoom('down')


def start_focus_positive():
    settings.start_focus()


def stop_focus_positive():
    settings.stop_focus()


def start_focus_down():
    settings.start_focus('down')


def stop_focus_down():
    settings.stop_focus('down')


def is_hdmi():
    return settings.get_projector_settings()['media_block'] == 'UNKNOWN'