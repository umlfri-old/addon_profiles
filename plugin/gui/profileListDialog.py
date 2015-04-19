import os
from imports.gtk2 import gtk, gobject
from util import FixTreeViewSelectionOnRightClick


class CProfileListDialog(object):

    gladeFile = os.path.join(os.path.dirname(__file__), "profileListDialog.glade")

    def __init__(self):

        self.wTree = gtk.Builder()
        self.wTree.add_from_file(self.gladeFile)

        signals = {
            'tvProfiles_button_press_event': self.tvProfiles_button_press_event_handler
        }

        self.wTree.connect_signals(signals)

        self.__dialog = self.wTree.get_object('profileListDialog')
        self.__tvProfiles = self.wTree.get_object('tvProfiles')
        self.__profileList = self.__tvProfiles.get_model()
        self.__profileList.clear()
        self.__profileListPopupMenu = self.wTree.get_object('profileListPopupMenu')
        self.__removeProfileMenuItem = self.wTree.get_object('removeProfileMenuItem')

    def Show(self):
        self.__FillProfiles()

        result = self.__dialog.run()
        self.__dialog.hide()
        if result == 0:
            return None
        else:
            return None

    def __FillProfiles(self):
        profiles = ['prof1', 'test', 'ppp']
        for profile in profiles:
            self.__profileList.append([profile])

    def tvProfiles_button_press_event_handler(self, widget, event):
        if event.button == 3:
            FixTreeViewSelectionOnRightClick(self.__tvProfiles, int(event.x), int(event.y))

            self.__UpdateProfileListContextMenu()

            self.__profileListPopupMenu.popup(None, None, None, event.button, event.time)

            return True

    def __UpdateProfileListContextMenu(self):
        selection = self.__tvProfiles.get_selection()
        selectedItemsCount = selection.count_selected_rows()

        canRemoveProfile = selectedItemsCount > 0

        self.__removeProfileMenuItem.set_sensitive(canRemoveProfile)
