# -*- coding: utf-8 -*-

"""
Copyright (c) 2015 Federico Vaga <federico.vaga@gmail.com>
License GNU Public License v3
"""

from ConfigParser import ConfigParser
import toggl
import os

class PlasmogglConfigManager():
    PLASMOGGL_CONFIG_FILE = "~/.plasmogglcfg"

    def __init__(self):
        # Retreive configuration from toggl-cli config file
        self.settings = {}
        self.settings["api_token"] = str(toggl.Config()
                                         .get("auth", "api_token"))
        self.settings["login"] = str(toggl.Config()
                                     .get("auth", "username"))
        self.settings["password"] = str(toggl.Config()
                                        .get("auth", "password"))
        self.settings["prefer_token"] = bool(toggl.Config()
                                             .get("options", "prefer_token"))

        self.cfg = ConfigParser()
        self.cfg.read(os.path.expanduser(self.PLASMOGGL_CONFIG_FILE))
        if not self.cfg.has_section("plasmoggl"):
            self.cfg.add_section("plasmoggl")

        if not self.cfg.has_option("plasmoggl", "show_elapsed"):
            self.cfg.set("plasmoggl", "show_elapsed", "false")
        self.settings["show_elapsed"] = self.cfg.get("plasmoggl", "show_elapsed").lower() == "true"

        if not self.cfg.has_option("plasmoggl", "show_seconds"):
            self.cfg.set("plasmoggl", "show_seconds", "false")
        self.settings["show_seconds"] = self.cfg.get("plasmoggl", "show_seconds").lower() == "true"

        if not self.cfg.has_option("plasmoggl", "refresh_period"):
            self.cfg.set("plasmoggl", "refresh_period", "30")
        self.settings["refresh_period"] = int(self.cfg.get("plasmoggl",
                                                           "refresh_period"))

        # If the configuration is not valid, then open the configuration
        # interface
        try:
            toggl.Config().validate_auth()
        except Exception as e:
            self.showConfigurationInterfaces()

    def _save_config_toggl_cli(self):
        """
        It save the toggl-cli configuration
        """
        if "login" in self.settings:
            toggl.Config().set("auth", "username",
                               self.settings["login"])
        if "password" in self.settings:
            toggl.Config().set("auth", "password",
                               self.settings["password"])
        if "api_token" in self.settings:
            toggl.Config().set("auth", "api_token",
                               self.settings["api_token"])
        if "prefer_token" in self.settings:
            toggl.Config().set("options", "prefer_token",
                               self.settings["prefer_token"])
        toggl.Config().store()

    def _save_config_plasmoggl(self):
        """
        It saves the plasmoggl configuration
        """
        if "show_elapsed" in self.settings:
            self.cfg.set("plasmoggl", "show_elapsed",
                         self.settings["show_elapsed"])
        if "show_seconds" in self.settings:
            self.cfg.set("plasmoggl", "show_seconds",
                         self.settings["show_seconds"])
        if "refresh_period" in self.settings:
            self.cfg.set("plasmoggl", "refresh_period",
                         self.settings["refresh_period"])

        with open(os.path.expanduser(self.PLASMOGGL_CONFIG_FILE), 'w') as f:
            self.cfg.write(f)
        os.chmod(os.path.expanduser(self.PLASMOGGL_CONFIG_FILE), 0600)

    def updateConfiguration(self, newValues):
        # Toggl integration
        self.settings.update(newValues)
        self._save_config_toggl_cli()
        self._save_config_plasmoggl()

    def get(self, name):
        return self.settings[name]

    def getAll(self):
        return self.settings
