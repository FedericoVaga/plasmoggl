Author: Federico Vaga <federico.vaga@gmail.com>

This is a KDE plasmoid for the Toggl[1] web service. You can find the
the source code repository on github at the following address:

   https://github.com/FedericoVaga/plasmoggl


INSTALLATION
------------
All the package management can be done with the project Make file

You can install the plasmoid on your desktop:

    make install

You can uninstall the plasmoid from your desktop:

    make uninstall

If you already have an older version of the plasmoid, you can update it:

    make update


CHANGE LOG
----------

1.0
- basic task entry


DEPENDENCIES
------------
The plasmoid is written in Python using PyQT4 and PyKDE4. For the toggl interface it uses classes from the toggl-cli[2] project.


REFERENCES
----------

[1] https://www.toggl.com/
[2] https://github.com/drobertadams/toggl-cli