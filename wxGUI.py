#!/usr/bin/python
# -*- coding: utf-8 -*-
import wx
from r515.projector import *
import ConfigParser


class MainWindow(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"R515 µTMS", pos=wx.DefaultPosition, size=wx.Size(640, 480),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)

        self.timer = wx.Timer(self, wx.ID_ANY)
        self.timer.Start(1000)
        self.Bind(wx.EVT_TIMER, self.update_time, self.timer)

        # Setting up the menu.
        mainMenu = wx.Menu()

        # wx.ID_ABOUT and wx.ID_EXIT are standard ids provided by wxWidgets.
        menuAbout = mainMenu.Append(wx.ID_ABOUT, "&About"," Information about this program")
        menuExit = mainMenu.Append(wx.ID_EXIT,"E&xit"," Terminate the program")

        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(mainMenu,"&R515") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        self.mainTool = self.CreateToolBar(wx.TB_FLAT | wx.TB_HORIZONTAL, wx.ID_ANY)
        self.play = self.mainTool.AddLabelTool(wx.ID_ANY, u"Play",
                                               wx.Bitmap(u"res/play.png", wx.BITMAP_TYPE_ANY),
                                               wx.NullBitmap, wx.ITEM_NORMAL, u"Play", u"Play current SPL/CPL", None)

        self.pause = self.mainTool.AddLabelTool(wx.ID_ANY, u"Pause",
                                                wx.Bitmap(u"res/pause.png",
                                                          wx.BITMAP_TYPE_ANY), wx.NullBitmap, wx.ITEM_NORMAL, u"Pause",
                                                u"Pauses Playback", None)

        self.stop = self.mainTool.AddLabelTool(wx.ID_ANY, u"Stop",
                                               wx.Bitmap(u"res/stop.png", wx.BITMAP_TYPE_ANY),
                                               wx.NullBitmap, wx.ITEM_NORMAL, u"Stop",
                                               u"Stop current Playback and close douser", None)

        self.mainTool.AddSeparator()

        self.closeDouser = self.mainTool.AddLabelTool(wx.ID_ANY, u"Close Douser",
                                                      wx.Bitmap(u"res/close.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap,
                                                      wx.ITEM_NORMAL, u"Close Douser", u"Closes the douser", None)

        self.openDouser = self.mainTool.AddLabelTool(wx.ID_ANY, u"Open Douser",
                                                     wx.Bitmap(u"res/open.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap,
                                                     wx.ITEM_NORMAL, u"Open Douser", u"Open the douser", None)

        self.mainTool.AddSeparator()

        self.stereo = self.mainTool.AddLabelTool(wx.ID_ANY, u"Stereo", wx.Bitmap(u"res/stereo.png", wx.BITMAP_TYPE_ANY),
                                                 wx.NullBitmap, wx.ITEM_NORMAL, u"Stereo", u"Select Stereo", None)

        self.surroundFive = self.mainTool.AddLabelTool(wx.ID_ANY, u"5.1", wx.Bitmap(u"res/5_1.png", wx.BITMAP_TYPE_ANY),
                                                       wx.NullBitmap, wx.ITEM_NORMAL, u"5.1", u"Select 5.1", None)

        self.surroundSeven = self.mainTool.AddLabelTool(wx.ID_ANY, u"7.1",
                                                        wx.Bitmap(u"res/7_1.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap,
                                                        wx.ITEM_NORMAL, u"7.1", u"Select 7.1", None)

        self.mainTool.AddSeparator()

        self.cinemascope = self.mainTool.AddLabelTool(wx.ID_ANY, u"Cinemascope",
                                                      wx.Bitmap(u"res/cs.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap,
                                                      wx.ITEM_NORMAL, u"Cinemascope", u"Cinemascope", None)

        self.flat = self.mainTool.AddLabelTool(wx.ID_ANY, u"Flat", wx.Bitmap(u"res/flat.png", wx.BITMAP_TYPE_ANY),
                                               wx.NullBitmap, wx.ITEM_NORMAL, u"Flat", u"Flat", None)

        self.cinemascopeHdmi = self.mainTool.AddLabelTool(wx.ID_ANY, u"HDMI Cinemascope",
                                                          wx.Bitmap(u"res/hdmi_cs.png", wx.BITMAP_TYPE_ANY),
                                                          wx.NullBitmap, wx.ITEM_NORMAL, u"HDMI Cinemascope",
                                                          u"HDMI 1 in Cinemascope", None)

        self.flatHdmi = self.mainTool.AddLabelTool(wx.ID_ANY, u"HDMI Flat",
                                                   wx.Bitmap(u"res/hdmi_flat.png", wx.BITMAP_TYPE_ANY), wx.NullBitmap,
                                                   wx.ITEM_NORMAL, u"HDMI Flat", u"HDMI 1 in Flat", None)

        self.mainTool.Realize()

        bSizer2 = wx.BoxSizer(wx.HORIZONTAL)

        self.libraryPanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        fgSizer2 = wx.FlexGridSizer(2, 1, 0, 0)
        fgSizer2.AddGrowableCol(0)
        fgSizer2.AddGrowableRow(1)
        fgSizer2.SetFlexibleDirection(wx.BOTH)
        fgSizer2.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_NONE)

        self.librarySearch = wx.SearchCtrl(self.libraryPanel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                           wx.DefaultSize, 0)
        self.librarySearch.ShowSearchButton(True)
        self.librarySearch.ShowCancelButton(False)
        fgSizer2.Add(self.librarySearch, 0, wx.EXPAND, 5)

        self.m_treeCtrl2 = wx.TreeCtrl(self.libraryPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                       wx.TR_DEFAULT_STYLE)
        fgSizer2.Add(self.m_treeCtrl2, 0, wx.EXPAND, 0)

        self.libraryPanel.SetSizer(fgSizer2)
        self.libraryPanel.Layout()
        fgSizer2.Fit(self.libraryPanel)
        bSizer2.Add(self.libraryPanel, 1, wx.EXPAND, 2)

        self.playlistPanel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        gSizer5 = wx.GridSizer(1, 1, 0, 0)

        m_listBox1Choices = []
        self.m_listBox1 = wx.ListBox(self.playlistPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                     m_listBox1Choices, 0)
        gSizer5.Add(self.m_listBox1, 0, wx.EXPAND, 5)

        self.playlistPanel.SetSizer(gSizer5)
        self.playlistPanel.Layout()
        gSizer5.Fit(self.playlistPanel)
        bSizer2.Add(self.playlistPanel, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer2)
        self.Layout()
        self.mainStatus = self.CreateStatusBar(1, wx.ST_SIZEGRIP, wx.ID_ANY)

        self.Centre(wx.BOTH)

    def __del__(self):
        pass

    def update_time(self, event):
        pass



#Load settings:   IP Adresse    Benutzer  Passwort
config = ConfigParser.ConfigParser()
config.read(['r515.cfg'])

conn = Connection(config.get('Connection', 'IP'), config.get('Connection', 'USR'), config.get('Connection', 'PWD'))
prj = BasicFunctions(conn)
settings = BasicSettings(conn)
library = Library(conn)

app = wx.App(False)
frame = MainWindow(None)
frame.Show()
app.MainLoop()