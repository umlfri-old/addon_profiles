from gui import CProfileListDialog
from ApplyProfilesExecutor import CApplyProfilesExecutor


class CAppliedProfileEditor(object):

    def __init__(self, interface):
        self.__interface = interface

    def EditProfiles(self):
        projectRoot = self.__interface.project.root

        applyProfilesExecutor = CApplyProfilesExecutor(projectRoot)

        appliedProfiles = applyProfilesExecutor.GetCurrentProfiles()
        availableProfiles = applyProfilesExecutor.GetAvailableProfiles()
        CProfileListDialog(projectRoot, appliedProfiles, availableProfiles).Show()