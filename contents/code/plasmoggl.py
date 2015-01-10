# -*- coding: utf-8 -*-

"""
Copyright (c) 2015 Federico Vaga <federico.vaga@gmail.com>
License GNU Public License v3
"""

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QGraphicsLinearLayout
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript

import toggl
import time

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class Plasmoggl(plasmascript.Applet):
    DEFAULT_PROJECT = "SELECT PROJECT"
    HEIGHT = "height: 32px;"

    def __init__(self,parent,args=None):
        plasmascript.Applet.__init__(self,parent)

    def init(self):
        self.setAspectRatioMode(Plasma.FixedSize)
        self.setHasConfigurationInterface(False)

        self.theme = Plasma.Svg(self)
        self.theme.setImagePath("widgets/background")
        self.setBackgroundHints(Plasma.Applet.DefaultBackground)

        self.layout = QGraphicsLinearLayout(Qt.Horizontal, self.applet)

        self.current_work = toggl.TimeEntryList().now()

        # Insert Task
        self.lineEdit = Plasma.LineEdit(self.applet)
        self.lineEdit.setClickMessage("What are you working on?")
        self.lineEdit.setStyleSheet("border: 1px solid black; width:300px;" +
                                    self.HEIGHT);
        self.layout.addItem(self.lineEdit)

        self.projectCombo = Plasma.ComboBox(self.applet)
        self.projectCombo.addItem("SELECT PROJECT")
        for pj in toggl.ProjectList().project_list:
            self.projectCombo.addItem(pj["name"])
        self.projectCombo.setStyleSheet("border: 1px solid black;" +
                                        self.HEIGHT);
        self.layout.addItem(self.projectCombo)

        # Start and Stop button
        self.startButton = Plasma.PushButton(self.applet)
        self.startButton.clicked.connect(self.__toggle_working)
        self.layout.addItem(self.startButton)

        # Add Layout to the applet
        self.applet.setLayout(self.layout)
        self.__guiUpdate()

    def _fill_project_combo(self, cmb):
        prj = toggl.ProjectList()
        cmb.addItem("---")
        for project in prj.project_list:
            cmb.addItem(project['name'])

    def __toggle_working(self):
        """
        It starts and stops an activity (a.k.a. work)
        """
        #self.current_work = toggl.TimeEntryList().now()
        if self.current_work is not None:
            self.current_work.stop()
        else:
            self.current_work = toggl.TimeEntry(description=str(self.lineEdit.text()),
                                                project_name=str(self.projectCombo.text()))
            self.current_work.start()

        # Update interface
        self.__guiUpdate()

    def __guiUpdate(self):
        """
        Update the user interface according to the Toggl status
        """

        toggl.TimeEntryList().reload()
        self.current_work = toggl.TimeEntryList().now()
        if self.current_work is not None:
            self.lineEdit.setText(self.current_work.get('description'))
            self.startButton.setText("Stop")
            btnStyle = "background-color:#FF0000;"
            pid = self.current_work.get("pid")
            prj = toggl.ProjectList().find_by_id(pid)
        else:
            self.lineEdit.setText("")
            self.startButton.setText("Start")
            btnStyle = "background-color:#4bc800;"
            prj = None

        btnStyle += "border: 1px solid black; color: #FFFFFF; padding: 0 5px; "  + self.HEIGHT
        self.startButton.setStyleSheet(btnStyle)

        if prj is not None:
            self.projectCombo.nativeWidget().setCurrentItem(prj["name"])
        else:
            self.projectCombo.nativeWidget().setCurrentItem("SELECT PROJECT")


def CreateApplet(parent):
    return Plasmoggl(parent)
