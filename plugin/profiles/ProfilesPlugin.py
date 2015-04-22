from ..gui import CProfileListDialog


class CProfilesPlugin(object):

    def __init__(self, interface):
        self.__interface = interface

        self.__interface.add_notification('project-opened', self.__OnProjectOpened)

        self.__CreateToolbarButtons()
        self.__UpdateButtonVisibility()

    def __OnProjectOpened(self):
        self.__UpdateButtonVisibility()

    def __UpdateButtonVisibility(self):
        project = self.__interface.project
        if project is not None and project.metamodel.uri == "urn:umlfri.org:metamodel:uml":
            self.__changeAppliedProfilesButton.visible = True
        else:
            self.__changeAppliedProfilesButton.visible = False

    def __CreateToolbarButtons(self):
        self.__changeAppliedProfilesButton = self.__interface.gui_manager.button_bar.add_button(
            'ChangeAppliedProfiles',
            lambda *a: self.__ShowProfileListDialog(),
            -1,
            'Profiles'
        )

    def __ShowProfileListDialog(self):
        CProfileListDialog(self.__interface.project.root).Show()