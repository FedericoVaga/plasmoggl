# -*- coding: utf-8 -*-

"""
Copyright (c) 2015 Federico Vaga <federico.vaga@gmail.com>
License GNU Public License v3
"""

from PyQt4.QtGui import *
from plasmoggl_configui import Ui_PlasmogglConfigDialog

class PlasmogglConfigDialog(QWidget, Ui_PlasmogglConfigDialog):
    def __init__(self, parent, settings):
        QWidget.__init__(self)
        self.parent = parent
        self.setupUi(self)

        if 'show_seconds' in settings:
            self.showSeconds.setChecked(settings['show_seconds'])
        if 'show_elapsed' in settings:
            self.showElapsed.setChecked(settings['show_elapsed'])
        if 'refresh_period' in settings:
            self.refreshPeriod.setValue(settings['refresh_period'])

        self.showElapsed.toggled.connect(self._showElapsedChange)
        self.showSeconds.setEnabled(self.showElapsed.isChecked())

    def _showElapsedChange(self, checked):
        self.showSeconds.setEnabled(checked)

    def exportSettings(self):
        return {
            'show_seconds': self.showSeconds.isChecked(),
            'show_elapsed': self.showElapsed.isChecked(),
        }
