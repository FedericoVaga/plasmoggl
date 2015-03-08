# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'plasmoggl_config.ui'
#
# Created: Sun Mar  8 19:52:06 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_PlasmogglConfigDialog(object):
    def setupUi(self, PlasmogglConfigDialog):
        PlasmogglConfigDialog.setObjectName(_fromUtf8("PlasmogglConfigDialog"))
        PlasmogglConfigDialog.resize(222, 103)
        self.formLayoutWidget = QtGui.QWidget(PlasmogglConfigDialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 5, 188, 69))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout_2 = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout_2.setMargin(0)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.showElapsedLabel = QtGui.QLabel(self.formLayoutWidget)
        self.showElapsedLabel.setObjectName(_fromUtf8("showElapsedLabel"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.showElapsedLabel)
        self.showElapsed = QtGui.QCheckBox(self.formLayoutWidget)
        self.showElapsed.setText(_fromUtf8(""))
        self.showElapsed.setObjectName(_fromUtf8("showElapsed"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.showElapsed)
        self.showSecondLabel = QtGui.QLabel(self.formLayoutWidget)
        self.showSecondLabel.setObjectName(_fromUtf8("showSecondLabel"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.showSecondLabel)
        self.showSeconds = QtGui.QCheckBox(self.formLayoutWidget)
        self.showSeconds.setText(_fromUtf8(""))
        self.showSeconds.setObjectName(_fromUtf8("showSeconds"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.showSeconds)
        self.refreshPeriodLabel = QtGui.QLabel(self.formLayoutWidget)
        self.refreshPeriodLabel.setObjectName(_fromUtf8("refreshPeriodLabel"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.LabelRole, self.refreshPeriodLabel)
        self.refreshPeriod = QtGui.QSpinBox(self.formLayoutWidget)
        self.refreshPeriod.setObjectName(_fromUtf8("refreshPeriod"))
        self.formLayout_2.setWidget(2, QtGui.QFormLayout.FieldRole, self.refreshPeriod)

        self.retranslateUi(PlasmogglConfigDialog)
        QtCore.QMetaObject.connectSlotsByName(PlasmogglConfigDialog)

    def retranslateUi(self, PlasmogglConfigDialog):
        PlasmogglConfigDialog.setWindowTitle(_translate("PlasmogglConfigDialog", "Form", None))
        self.showElapsedLabel.setText(_translate("PlasmogglConfigDialog", "Show elapsed time:", None))
        self.showSecondLabel.setText(_translate("PlasmogglConfigDialog", "Show seconds", None))
        self.refreshPeriodLabel.setText(_translate("PlasmogglConfigDialog", "Refresh period (s)", None))

