# -*- coding: utf-8 -*-

"""
Copyright (c) 2015 Federico Vaga <federico.vaga@gmail.com>
License GNU Public License v3
"""

from PyQt4.QtGui import *
from configui import Ui_PlasmogglConfigDialog

class ConfigDialog(QWidget, Ui_PlasmogglConfigDialog):
    def __init__(self, parent, settings):
        QWidget.__init__(self)
        self.parent = parent
        self.setupUi(self)

        if 'api_token' in settings:
            self.api.setText(settings['api_token'])
        if 'prefer_token' in settings:
            self.ptoken.setChecked(settings['prefer_token'])
        if 'login' in settings:
            self.login.setText(settings['login'])
        if 'password' in settings:
            self.password.setText(settings['password'])

    def exportSettings(self):
        return {
            'api_token': str(self.api.text()),
            'login': str(self.login.text()),
            'password': str(self.password.text()),
            'prefer_token': str(self.ptoken.isChecked()),
        }
