from gui import CProfileListDialog
from ApplyProfilesExecutor import CApplyProfilesExecutor, ApplyProfilesExecutorError


class CAppliedProfileEditor(object):

    def __init__(self, interface):
        self.__interface = interface

    def EditProfiles(self):
        project = self.__interface.project
        projectRoot = project.root

        applyProfilesExecutor = CApplyProfilesExecutor(project)

        appliedProfiles = applyProfilesExecutor.GetCurrentProfiles()
        availableProfiles = applyProfilesExecutor.GetAvailableProfiles()
        dialog = CProfileListDialog(projectRoot, appliedProfiles, list(availableProfiles))
        if not dialog.Show():
            return

        applyProfilesExecutor.SetAppliedProfiles(appliedProfiles)

        try:
            with self.__interface.transaction:
                applyProfilesExecutor.ApplyProfiles()
        except ApplyProfilesExecutorError as e:
            print(repr(e.GetInnerException()))
            self.__interface.gui_manager.display_warning(
                'Error occurred while applying profiles: \n\n{0}'.format(e.GetInnerExceptionMessage()))