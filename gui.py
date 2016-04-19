#!/usr/bin/python
# -*- coding: utf-8 -*-

from Tkinter import *
from r515.projector import *
import time
import ConfigParser

class Application(Frame):
    def _ms_to_tc(self, ms):
        #ms = int(ms)
        seconds = ms / 1000
        hours = seconds/3600
        minutes = (seconds%3600)/60
        seconds = seconds%60
        return '%(hours)02d:%(minutes)02d:%(seconds)02d' % {"hours": hours, "minutes": minutes, "seconds": seconds}
        
    def sync_time(self):
        info = self._values
        if info["uuid"] != None:
            if info["typ"] == "CPL":
                self._remaining_cpl = int(info["time"]["remaining"])
                self.cpl_time["text"] = "DCP verbleibend: " + self._ms_to_tc(self._remaining_cpl)
                self.spl_time["text"] = "Playlist verbleibend: 00:00:00"
                self.spl_name["text"] = "Keine Playlist ausgewählt"
            elif info["typ"] == "SPL":
                self._remaining_spl = int(info["time"]["remaining"])
                self.spl_time["text"] = "Playlist verbleibend: " + self._ms_to_tc(self._remaining_spl)
                if self._cpl != None:
                    self._remaining_cpl = self._cpl["duration"] - (int(info["time"]["elapsed"]) - self._cpl["offset"])
                    self.cpl_time["text"] = "DCP verbleibend: " + self._ms_to_tc(self._remaining_cpl)

    def sync_playlist(self):
        playlist = Playlist(conn, self._values["uuid"])
        self._cpl = playlist.get_cpl_at_offset(self._values["time"]["elapsed"])
        self.spl_name["text"] = playlist.get_title()
        if self._cpl != None:
            self.cpl_name["text"] = library.get_cpl_info(self._cpl["uuid"])["title"]
                
    def update_time(self):
        if self._playing:
            self._remaining_cpl = self._remaining_cpl - 1000
            self.cpl_time["text"] = "DCP verbleibend: " + self._ms_to_tc(self._remaining_cpl)
            if self._values["typ"] == "SPL":
                self._remaining_spl = self._remaining_spl - 1000
                self.spl_time["text"] = "Playlist verbleibend: " + self._ms_to_tc(self._remaining_spl)
            if self._remaining_cpl - 1000 <= 100:
                if self._values["typ"] == "SPL":
                    self._values = prj.get_show_info()
                    self.sync_playlist()
                    self.sync_time()
                else:
                    self.sync_status(False)
        self.after(1000, self.update_time)

    def sync_status(self, loop = True):
        current_settings = settings.get_projector_settings()
        self._values = prj.get_show_info()
        self.sync_time()
        values = self._values        
        self.status["text"] = values["status"]
        if values["status"] == "STOPPED" or values["status"] == "PAUSED" or values["status"] == "COMPLETED":
            self.play["text"] = "Play"
            self._playing = False
        elif values["status"] == "PLAYING":
            self.play["text"] = "Pause"
            self._playing = True
        if current_settings["picture_mode"] == "0":
            self.format["text"] = "DCI Flat"
        elif current_settings["picture_mode"] == "1":
            self.format["text"] = "DCI CS"
        elif current_settings["picture_mode"] == "2":
            self.format["text"] = "HDMI Flat"
        elif current_settings["picture_mode"] == "3":
            self.format["text"] = "HDMI CS"
        if values["typ"] == "CPL":
            self.cpl_name["text"] = library.get_cpl_info(values["uuid"])["title"]
        elif values["typ"] == "SPL":
            self.sync_playlist()
        if loop:
            self.after(30000, self.sync_status)

    def update_power(self):
        status = prj.get_power_status()
        if status == "STANDBY":
            self.power["text"] = "Lampe anschalten"
        elif status == "ON":
            self.power["text"] = "Lampe ausschalten"
        else:
            self.power["text"] = status
        self.after(40000, self.update_power)
        
    def play_toggle(self):
        status = self._values["status"]
        if status == "STOPPED" or status == "NONE" or status == "COMPLETED":
            prj.play()
        elif status == "PLAYING":
            prj.pause()
        elif status == "PAUSED":
            prj.resume()
        self.after(800, self.sync_status(False))

    def power_toggle(self):
        status = prj.get_power_status()        
        if status == "STANDBY":
            prj.power_on()
            self.power["text"] = "WARM_UP"
        elif status == "ON":
            prj.power_standby()
            self.power["text"] = "COOLING"
        else:
            self.power["text"] = status
    
    def stop_command(self):
        prj.stop()
        self.after(2000, self.sync_status(False))
        
    def play_logo(self):
        prj.close_douser()
        prj.stop()
        if settings.get_projector_settings()["picture_mode"] != (int(config.get('Logo', 'Format'))-1):
            settings.load_format(int(config.get('Logo', 'Format')))
            print "Format", (int(config.get('Logo', 'Format'))-1)
            #time.sleep(3)
        status = prj.get_show_info()["status"]
        while not (status == "STOPPED" or status == "NONE" or status == "COMPLETED"):
            status = prj.get_show_info()["status"]
        time.sleep(0.8)
        prj.play(config.get('Logo', 'UUID'), "CPL", 0)
        if config.get('Logo', 'Loop') == "False":
            time.sleep(4)
            prj.pause()
        prj.open_douser()
        self.after(800, self.sync_status(False))
        
    def toggle_douser(self):
        if self._douser:
            prj.open_douser()
        else:
            prj.close_douser()
        self._douser = not self._douser

    def createWidgets(self):
        self.status = Label(self)
        self.status["text"] = "Stopped"
        self.status["justify"] = "center"
        self.status["padx"] = 10
    
        self.status.pack({"anchor": "n", "side": "top", "expand": 1, "fill":"x"})

        self.format = Label(self)
        self.format["text"] = "DCI Flat"
        self.format["justify"] = "center"
        self.format["padx"] = 10

        self.format.pack({"anchor": "n", "side": "top", "expand": 1, "fill":"x"})

        self.spl_name = Label(self)
        self.spl_name["text"] = "Keine Playlist ausgewählt"
        self.spl_name["justify"] = "center"
        self.spl_name["padx"] = 10

        self.spl_name.pack({"anchor": "n", "side": "top", "expand": 1, "fill":"x"})

        self.spl_time = Label(self)
        self.spl_time["text"] = "Playlist verbleibend: 00:00:00"
        self.spl_time["justify"] = "center"
        self.spl_time["padx"] = 10

        self.spl_time.pack({"anchor": "n", "side": "top", "expand": 1, "fill":"x"})

        self.cpl_name = Label(self)
        self.cpl_name["text"] = "Keine DCP ausgewählt"
        self.cpl_name["justify"] = "center"
        self.cpl_name["padx"] = 10

        self.cpl_name.pack({"anchor": "n", "side": "top", "expand": 1, "fill":"x"})

        self.cpl_time = Label(self)
        self.cpl_time["text"] = "DCP verbleibend: 00:00:00"
        self.cpl_time["justify"] = "center"
        self.cpl_time["padx"] = 10

        self.cpl_time.pack({"anchor": "n", "side": "top", "expand": 1, "fill":"x"})

        self.play = Button(self)
        self.play["text"] = "Play"
        self.play["command"] = self.play_toggle

        self.play.pack({"anchor": "n", "side": "top", "expand": 1, "fill":"x"})

        self.stop = Button(self)
        self.stop["text"] = "Stop"
        self.stop["command"] = self.stop_command

        self.stop.pack({"anchor": "n", "side": "top", "expand": 1, "fill":"x"})

        self.open_douser = Button(self)
        self.open_douser["text"] = "Klappe öffnen"
        self.open_douser["command"] = prj.open_douser

        self.open_douser.pack({"anchor": "n", "side": "top", "expand": 1, "fill":"x"})

        self.close_douser = Button(self)
        self.close_douser["text"] = "Klappe schließen"
        self.close_douser["command"] = prj.close_douser

        self.close_douser.pack({"anchor": "n", "side": "top", "expand": 1, "fill":"x"})
        
        self.dci_flat = Button(self)
        self.dci_flat["text"] = "DCI Flat"
        self.dci_flat["command"] = lambda: settings.load_format(1)

        self.dci_flat.pack({"anchor": "n", "side": "top", "expand": 1, "fill":"x"})

        self.dci_cs = Button(self)
        self.dci_cs["text"] = "DCI CS"
        self.dci_cs["command"] = lambda: settings.load_format(2)

        self.dci_cs.pack({"anchor": "n", "side": "top", "expand": 1, "fill":"x"})

        self.hdmi_flat = Button(self)
        self.hdmi_flat["text"] = "HDMI Flat"
        self.hdmi_flat["command"] = lambda: settings.load_format(3)

        self.hdmi_flat.pack({"anchor": "n", "side": "top", "expand": 1, "fill":"x"})

        self.hdmi_cs = Button(self)
        self.hdmi_cs["text"] = "HDMI CS"
        self.hdmi_cs["command"] = lambda: settings.load_format(4)

        self.hdmi_cs.pack({"anchor": "n", "side": "top", "expand": 1, "fill":"x"})

        self.power = Button(self)
        self.power["text"] = "Lampe anschalten"
        self.power["command"] = self.power_toggle

        self.power.pack({"anchor": "n", "side": "top", "expand": 1, "fill":"x"})
        
        self.logo = Button(self)
        self.logo["text"] = "Instant Logo"
        self.logo["command"] = self.play_logo

        self.logo.pack({"anchor": "n", "side": "top", "expand": 1, "fill":"x"})

    def __init__(self, master=None):
        self._cpl = None
        Frame.__init__(self, master)
        self.pack({"side": "top", "expand": 1, "fill":"both"})
        self.createWidgets()
        master.bind("p", lambda e: self.play_toggle())
        master.bind("l", lambda e: self.play_logo())
        master.bind("s", lambda e: self.stop())
        master.bind("1", lambda e: settings.load_format(1))
        master.bind("2", lambda e: settings.load_format(2))
        master.bind("3", lambda e: settings.load_format(3))
        master.bind("4", lambda e: settings.load_format(4))
        master.bind("<space>", lambda e: self.toggle_douser())
        self._douser = False
        self.after(0, self.sync_status)
        self.after(0, self.sync_time)
        self.after(0, self.update_power)
        self.after(1000, self.update_time)
        
class Library_Window(Frame):

    def load_dcp(self):
        self.dcp["state"] = DISABLED
        self.spl["state"] = NORMAL
        self.table.delete(0, self.table.size()-1)
        self.table.bind("<Double-Button-1>", (lambda e: self.play(e, "CPL")))
        self._list = library.get_cpl_list()
        for cpl in self._list:
            self.table.insert(END, cpl['title'])

    def load_spl(self):
        self.spl["state"] = DISABLED
        self.dcp["state"] = NORMAL
        self.table.delete(0, self.table.size()-1)
        self.table.bind("<Double-Button-1>", (lambda e: self.play(e, "SPL")))
        self._list = library.get_spl_list()
        for cpl in self._list:
            self.table.insert(END, cpl['title'])
        
    def play(self, event, typ):
        #prj.close_douser()
        #prj.stop()
        #status = prj.get_show_info()["status"]
        #while not (status == "STOPPED" or status == "NONE" or status == "COMPLETED"):
        #    status = prj.get_show_info()["status"]
        #time.sleep(0.5)
        #prj.play(self._list[int(self.table.curselection()[0])]["uuid"], typ, 0)
        print self._list[int(self.table.curselection()[0])]["uuid"]
        #prj.open_douser()
        #self.after(800, app.sync_status(False))
        
    def createWidgets(self):
        self.pane = PanedWindow(self)
        self.pane["showhandle"] = True
        
        self.pane.pack({"anchor": "n", "side": "top", "expand": 1, "fill":"both"})
        
        self.button_frame = Frame(self.pane)

        self.button_frame.pack({"anchor": "n", "side": "top"})
        self.pane.add(self.button_frame)
        
        self.dcp = Button(self.button_frame)
        self.dcp["text"] = "DCP"
        self.dcp["justify"] = "center"
        self.dcp["padx"] = 10
        self.dcp["command"] = self.load_dcp

        self.dcp.pack({"anchor": "n", "side": "top", "expand": 0, "fill":"x"})

        self.spl = Button(self.button_frame)
        self.spl["text"] = "Playlist"
        self.spl["justify"] = "center"
        self.spl["padx"] = 10
        self.spl["command"] = self.load_spl
        
        self.button_frame["height"] = 50

        self.spl.pack({"anchor": "n", "side": "top", "expand": 0, "fill":"x"})

        self.table_frame = LabelFrame(self.pane)
        self.table_frame["text"] = "DCP Auswahl (Start durch Doppelklick)"

        self.table_frame.pack({"anchor": "n", "side": "top", "expand": 1, "fill":"both"})
        self.pane.add(self.table_frame)
        
        self.scrollbar = Scrollbar(self.table_frame)
        self.scrollbar.pack({"side": "right", "fill": "y"})
        
        self.table = Listbox(self.table_frame)
        self.table["yscrollcommand"] = self.scrollbar.set
        self.scrollbar["command"] = self.table.yview
        
        self.table.pack({"anchor": "n", "side": "left", "expand": 1, "fill":"both"})
 
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack({"side": "top", "expand": 1, "fill":"both"})
        self.createWidgets()

#Load settings:   IP Adresse    Benutzer  Passwort
config = ConfigParser.ConfigParser()
config.read(['r515.cfg'])

conn = Connection(config.get('Connection', 'IP'), config.get('Connection', 'USR'), config.get('Connection', 'PWD'))
prj = BasicFunctions(conn)
settings = BasicSettings(conn)
library = Library(conn)

root = Tk()
root.wm_title("R515 Control")
app = Application(master=root)
t = Toplevel(root)
t.wm_title("R515 Library")
l = Library_Window(t)
app.mainloop()
root.destroy()
