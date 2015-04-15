#!/usr/bin/python

from org.umlfri.api.mainLoops import GtkMainLoop

class pluginMain:
    """
    Main class of the plugin, it defines what happens during its loading and basic functionality.
    """

    def __init__(self, interface):
        """
        Constructor.
        @param interface: API adapter object
        """
        self.__interface = interface
        self.__interface.set_main_loop(GtkMainLoop())
