from gui import CProfileListDialog
from ApplyProfilesTransaction import CApplyProfilesTransaction


class CAppliedProfileEditor(object):

    def __init__(self, interface):
        self.__interface = interface

    def EditProfiles(self):
        projectRoot = self.__interface.project.root

        applyProfilesTransaction = CApplyProfilesTransaction(projectRoot)

        appliedProfiles = applyProfilesTransaction.GetCurrentProfiles()
        availableProfiles = applyProfilesTransaction.GetAvailableProfiles()
        CProfileListDialog(projectRoot, appliedProfiles, availableProfiles).Show()