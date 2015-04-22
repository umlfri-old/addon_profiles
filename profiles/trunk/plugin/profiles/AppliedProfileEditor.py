from ProfileManager import CProfileManager
from gui import CProfileListDialog


class CAppliedProfileEditor(object):

    __profileManager = CProfileManager()

    def __init__(self, interface):
        self.__interface = interface

    def EditProfiles(self):
        CProfileListDialog(self.__interface.project.root).Show()