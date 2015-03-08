# -*- coding: utf-8 -*-

"""
Copyright (c) 2015 Federico Vaga <federico.vaga@gmail.com>
License GNU Public License v3
"""

# KDE
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt, SIGNAL, QTime, pyqtSignature, QString
from PyQt4.QtGui import QGraphicsLinearLayout
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
from PyKDE4.kdeui import KPageDialog, KDialog, KIcon

# plasmoggl
from config.config import ConfigDialog
from config.plasmoggl_config import PlasmogglConfigDialog
from plasmoggl_config_manager import PlasmogglConfigManager
import toggl

# System
from ConfigParser import ConfigParser
import datetime
import time
import os

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class Plasmoggl(plasmascript.Applet):
    DEFAULT_PROJECT = "SELECT PROJECT"
    HEIGHT = "height: 32px;"
    BORDER = "border: 1px solid black;"

    def __init__(self, parent, args=None):
        plasmascript.Applet.__init__(self, parent)

    def init(self):
        self.configManager = PlasmogglConfigManager()

        self.setAspectRatioMode(Plasma.FixedSize)
        self.theme = Plasma.Svg(self)
        self.theme.setImagePath("widgets/background")
        self.setBackgroundHints(Plasma.Applet.DefaultBackground)

        self.layout = QGraphicsLinearLayout(Qt.Horizontal, self.applet)

        self.current_work = toggl.TimeEntryList().now()

        # Insert Task
        self.lineEdit = Plasma.LineEdit(self.applet)
        self.lineEdit.setClickMessage("What are you working on?")
        self.lineEdit.setStyleSheet("width:300px;" +
                                    self.HEIGHT + self.BORDER)
        self.layout.addItem(self.lineEdit)

        # workspace combo
        self.workspaceCombo = Plasma.ComboBox(self.applet)
        self.workspaceCombo.setStyleSheet(self.HEIGHT + self.BORDER)
        self.layout.addItem(self.workspaceCombo)

        # project combo
        self.projectCombo = Plasma.ComboBox(self.applet)
        self.projectCombo.setStyleSheet(self.HEIGHT + self.BORDER)
        self.layout.addItem(self.projectCombo)

        # Time Label
        self.timeLabel = Plasma.Label(self.applet)
        self.timeLabel.setStyleSheet("font-weight: bold;margin-left: 10px;" +
                                     self.HEIGHT)
        self.layout.addItem(self.timeLabel)

        # Start and Stop button
        self.startButton = Plasma.PushButton(self.applet)
        self.startButton.clicked.connect(self.__toggle_working)
        self.layout.addItem(self.startButton)

        # Add Layout to the applet
        self.applet.setLayout(self.layout)

        # Prepare time engine
        self.connectToEngine()

        # Set workspaces list
        for ws in toggl.WorkspaceList():
            self.workspaceCombo.addItem(ws["name"])
        self.workspaceCombo.textChanged.connect(self._workspace_change)
        self._workspace_change(self.workspaceCombo.text())

        self.__guiUpdate()

    def connectToEngine(self):
        """
        It prepares the time engine, if necessary
        """
        if not self.configManager.get("show_elapsed"):
            return

        self.timeEngine = self.dataEngine("time")
        if self.configManager.get("show_seconds"):
            self.timeEngine.connectSource("Local", self, 1000)
        else:
            self.timeEngine.connectSource("Local", self, 6000,
                                          Plasma.AlignToMinute)

    def createConfigurationInterface(self, parent):
        """
        It create the configuration dialog by adding the different sections
        """
        self.toggl_cli_config = ConfigDialog(self, self.configManager.getAll())
        widget = parent.addPage(self.toggl_cli_config, "Toggl integration")
        widget.setIcon(KIcon(self.package().path() +
                             "contents/images/toggl.png"))

        self.plasmoggl_config = PlasmogglConfigDialog(self, self.configManager.getAll())
        widget = parent.addPage(self.plasmoggl_config, "Plasmoggl")
        widget.setIcon(KIcon(self.package().path() +
                             "contents/images/plasmoggl.png"))

        self.connect(parent, SIGNAL("okClicked()"), self.configOK)
        self.connect(parent, SIGNAL("cancelClicked()"), self.configCancel)

    def showConfigurationInterfaces(self):
        """
        It shows the configuration dialog
        """
        dialog = KPageDialog()
        dialog.setFaceType(KPageDialog.List)
        dialog.setButtons(KDialog.ButtonCode(KDialog.Ok | KDialog.Cancel))
        self.createConfigurationInterface(dialog)
        dialog.exec_()

    def configOK(self):
        """
        It saves the configuration
        """
        self.configManager.updateConfiguration(self.toggl_cli_config.exportSettings())
        self.configManager.updateConfiguration(self.plasmoggl_config.exportSettings())
        # Changing Plasmoggl configuration need a GUI update
        self.__guiUpdate()

        self.toggl_cli_config.deleteLater()
        self.plasmoggl_config.deleteLater()

    def configCancel(self):
        """
        It simply close the configuration interface
        """
        self.pconfig.delateLater()
        self.plasmoggl_config.deleteLater()

    def _workspace_change(self, wname):
        """
        User has changed the workspace. So we have to update the project list
        """
        self.projectCombo.clear()
        toggl.ProjectList().fetch(wname)
        self.projectCombo.addItem("SELECT PROJECT")
        for pj in toggl.ProjectList():
            self.projectCombo.addItem(pj["name"])

    def _fill_project_combo(self, cmb):
        prj = toggl.ProjectList()
        cmb.addItem("---")
        for project in prj.project_list:
            cmb.addItem(project['name'])

    def __toggle_working(self):
        """
        It starts and stops an activity (a.k.a. work)
        """
        # gself.current_work = toggl.TimeEntryList().now()
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

            wid = self.current_work.get("wid")
            wrk = toggl.WorkspaceList().find_by_id(wid)
            self._workspace_change(wrk["name"])

            pid = self.current_work.get("pid")
            prj = toggl.ProjectList().find_by_id(pid)
            self.__guiUpdateTimeLabel(int(time.time()) +
                                      self.current_work.get("duration"))
        else:
            self.lineEdit.setText("")
            self.startButton.setText("Start")
            self.__guiUpdateTimeLabel(0)
            btnStyle = "background-color:#4bc800;"
            prj = None
            wrk = None

        btnStyle += "color: #FFFFFF; padding: 0 5px; "
        btnStyle += self.HEIGHT + self.BORDER
        self.startButton.setStyleSheet(btnStyle)

        if wrk is not None:
            self.workspaceCombo.nativeWidget().setCurrentItem(wrk["name"])

        if prj is not None:
            self.projectCombo.nativeWidget().setCurrentItem(prj["name"])
        else:
            self.projectCombo.nativeWidget().setCurrentItem("SELECT PROJECT")

    @pyqtSignature("dataUpdated(const QString &, const Plasma::DataEngine::Data &)")
    def dataUpdated(self, sourceName, data):
        """
        Data update ready
        """

        if int(time.time()) % self.configManager.get("refresh_period") == 0:
            self.__guiUpdate()

        if self.current_work is None:
            return  # timer is not running

        self.__guiUpdateTimeLabel(int(time.time())
                                  + self.current_work.get("duration"))

    def __guiUpdateTimeLabel(self, s):
        """
        It updates the elapsed timer
        """
        if self.configManager.get("show_seconds"):
            delta = datetime.timedelta(seconds=s)
            str_delta = str(delta)
        else:
            delta = datetime.timedelta(minutes=(s / 60))
            str_delta = str(delta)[0:-3] + ":--"
        self.timeLabel.setText(str_delta)


def CreateApplet(parent):
    """
    Main entry point of the plasmoid
    """
    return Plasmoggl(parent)
