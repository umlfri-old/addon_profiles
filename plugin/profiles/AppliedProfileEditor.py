from ProfileManager import CProfileManager
from gui import CProfileListDialog


class CAppliedProfileEditor(object):

    __profileManager = CProfileManager()

    def __init__(self, interface):
        self.__interface = interface

    def EditProfiles(self):
        projectRoot = self.__interface.project.root
        availableProfiles = self.__profileManager.GetAvailableProfiles(projectRoot)
        CProfileListDialog(projectRoot, availableProfiles.itervalues()).Show()