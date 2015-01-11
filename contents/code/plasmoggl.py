# -*- coding: utf-8 -*-

"""
Copyright (c) 2015 Federico Vaga <federico.vaga@gmail.com>
License GNU Public License v3
"""

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt, SIGNAL
from PyQt4.QtGui import QGraphicsLinearLayout
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
from PyKDE4.kdeui import KPageDialog, KDialog, KIcon

from config.config import ConfigDialog
from config.plasmoggl_config import PlasmogglConfigDialog
import toggl

from ConfigParser import ConfigParser
import os

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class Plasmoggl(plasmascript.Applet):
    DEFAULT_PROJECT = "SELECT PROJECT"
    HEIGHT = "height: 32px;"
    PLASMOGGL_CONFIG_FILE = "~/.plasmogglcfg"

    def __init__(self,parent,args=None):
        plasmascript.Applet.__init__(self,parent)

    def init(self):
        self.__loadConfiguration()

        self.setAspectRatioMode(Plasma.FixedSize)
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

        # Time Label
        self.timeLabel = Plasma.Label(self.applet)
        self.timeLabel.setText("00:00:00")
        self.timeLabel.setStyleSheet("margin-left: 10px;" + self.HEIGHT);
        self.layout.addItem(self.timeLabel)

        # Start and Stop button
        self.startButton = Plasma.PushButton(self.applet)
        self.startButton.clicked.connect(self.__toggle_working)
        self.layout.addItem(self.startButton)

        # Add Layout to the applet
        self.applet.setLayout(self.layout)

        self.__guiUpdate()

    def __loadConfiguration(self):
        """
        It loads the configuration from config files. This plasmoid is using
        two configurationf files. One from toggl-cli, and another one for this
        plasmoid. In order to keep the configuration in the same variable I am
        using self.setting dictionary
        """
        self.setHasConfigurationInterface(True)

        # Retreive configuration from toggl-cli config file
        self.settings = {}
        self.settings["api_token"] = str(toggl.Config().get("auth", "api_token"))
        self.settings["login"] = str(toggl.Config().get("auth", "username"))
        self.settings["password"] = str(toggl.Config().get("auth", "password"))
        self.settings["prefer_token"] = bool(toggl.Config().get("options", "prefer_token"))

        self.cfg = ConfigParser()
        self.cfg.read(os.path.expanduser(self.PLASMOGGL_CONFIG_FILE))
        if not self.cfg.has_section("plasmoggl"):
            self.cfg.add_section("plasmoggl")

        if not self.cfg.has_option("plasmoggl", "show_elapsed"):
            self.cfg.set("plasmoggl", "show_elapsed", False)
        self.settings["show_elapsed"] = self.cfg.get("plasmoggl", "show_elapsed").lower() == "true"

        if not self.cfg.has_option("plasmoggl", "show_seconds"):
            self.cfg.set("plasmoggl", "show_seconds", False)
        self.settings["show_seconds"] = self.cfg.get("plasmoggl", "show_seconds").lower() == "true"

        try:
            toggl.Config().validate_auth()
        except Exception as e:
            self.showConfigurationInterfaces()

    def createConfigurationInterface(self, parent):
        """
        It create the configuration dialog by adding the different sections
        """
        self.pconfig = ConfigDialog(self, self.settings)
        widget = parent.addPage(self.pconfig, "Toggl integration")
        widget.setIcon(KIcon(self.package().path() + "contents/images/toggl.png"))

        self.plasmoggl_config = PlasmogglConfigDialog(self, self.settings)
        widget = parent.addPage(self.plasmoggl_config, "Plasmoggl")
        widget.setIcon(KIcon(self.package().path() + "contents/images/plasmoggl.png"))

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
        # Toggl integration
        self.settings.update(self.pconfig.exportSettings())
        if "login" in self.settings:
            toggl.Config().set("auth", "username", self.settings["login"])
        if "password" in self.settings:
            toggl.Config().set("auth", "password", self.settings["password"])
        if "api_token" in self.settings:
            toggl.Config().set("auth", "api_token", self.settings["api_token"])
        if "prefer_token" in self.settings:
            toggl.Config().set("options", "prefer_token", self.settings["prefer_token"])
        toggl.Config().store()

        # Plasmoggl configuration
        self.settings.update(self.plasmoggl_config.exportSettings())
        if "show_elapsed" in self.settings:
            self.cfg.set("plasmoggl", "show_elapsed", self.settings["show_elapsed"])
        if "show_seconds" in self.settings:
            self.cfg.set("plasmoggl", "show_seconds", self.settings["show_seconds"])
        with open(os.path.expanduser(self.PLASMOGGL_CONFIG_FILE), 'w') as cfgfile:
            self.cfg.write(cfgfile)
        os.chmod(os.path.expanduser(self.PLASMOGGL_CONFIG_FILE), 0600)

        # Changing Plasmoggl configuration need a GUI update
        self.__guiUpdate()

        self.pconfig.deleteLater()

    def configCancel(self):
        """
        It simply close the configuration interface
        """
        self.pconfig.delateLater()

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
