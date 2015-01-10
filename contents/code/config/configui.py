# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'contents/code/config/config.ui'
#
# Created: Sat Jan 10 16:06:18 2015
#      by: PyQt4 UI code generator 4.10.2
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
        PlasmogglConfigDialog.resize(345, 119)
        self.horizontalLayout = QtGui.QHBoxLayout(PlasmogglConfigDialog)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.api = QtGui.QLineEdit(PlasmogglConfigDialog)
        self.api.setToolTip(_fromUtf8(""))
        self.api.setWhatsThis(_fromUtf8(""))
        self.api.setEchoMode(QtGui.QLineEdit.Normal)
        self.api.setObjectName(_fromUtf8("api"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.api)
        self.apiLabel = QtGui.QLabel(PlasmogglConfigDialog)
        self.apiLabel.setObjectName(_fromUtf8("apiLabel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.apiLabel)
        self.loginLabel = QtGui.QLabel(PlasmogglConfigDialog)
        self.loginLabel.setObjectName(_fromUtf8("loginLabel"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.loginLabel)
        self.login = QtGui.QLineEdit(PlasmogglConfigDialog)
        self.login.setObjectName(_fromUtf8("login"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.login)
        self.PasswordLabel = QtGui.QLabel(PlasmogglConfigDialog)
        self.PasswordLabel.setObjectName(_fromUtf8("PasswordLabel"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.PasswordLabel)
        self.password = QtGui.QLineEdit(PlasmogglConfigDialog)
        self.password.setEchoMode(QtGui.QLineEdit.Password)
        self.password.setObjectName(_fromUtf8("password"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.password)
        self.preferLabel = QtGui.QLabel(PlasmogglConfigDialog)
        self.preferLabel.setObjectName(_fromUtf8("preferLabel"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.preferLabel)
        self.ptoken = QtGui.QCheckBox(PlasmogglConfigDialog)
        self.ptoken.setText(_fromUtf8(""))
        self.ptoken.setObjectName(_fromUtf8("ptoken"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.ptoken)
        self.horizontalLayout.addLayout(self.formLayout)

        self.retranslateUi(PlasmogglConfigDialog)
        QtCore.QMetaObject.connectSlotsByName(PlasmogglConfigDialog)

    def retranslateUi(self, PlasmogglConfigDialog):
        self.apiLabel.setText(_translate("PlasmogglConfigDialog", "API token", None))
        self.loginLabel.setText(_translate("PlasmogglConfigDialog", "Login:", None))
        self.PasswordLabel.setText(_translate("PlasmogglConfigDialog", "Password:", None))
        self.preferLabel.setText(_translate("PlasmogglConfigDialog", "Use token:", None))

