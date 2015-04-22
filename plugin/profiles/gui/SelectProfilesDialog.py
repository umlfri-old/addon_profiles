import os
from imports.gtk2 import gtk


class CSelectProfilesDialog(object):

    gladeFile = os.path.join(os.path.dirname(__file__), "selectProfilesDialog.glade")

    def __init__(self):

        self.wTree = gtk.Builder()
        self.wTree.add_from_file(self.gladeFile)

        self.__dialog = self.wTree.get_object('selectProfilesDialog')
        self.__tvProfiles = self.wTree.get_object('tvProfiles')
        self.__profileListStore = gtk.ListStore(str, object)
        self.__tvProfiles.set_model(self.__profileListStore)
        self.__profileList = self.__tvProfiles.get_model()
        self.__profileList.clear()

    def ChooseProfile(self, profiles):
        self.__FillProfiles(profiles)
        result = self.__dialog.run()
        self.__dialog.hide()
        if result == 0:
            return None
        else:
            return None

    def __GetSelectedProfile(self):
        iter = self.__profileListStore.get_selection().get_selected()[1]
        if iter is None:
            return None
        profile, = self.__profileListStore.get(iter, 1)
        return profile

    def __FillProfiles(self, profiles):
        for profile in profiles:
            self.__profileList.append([profile.GetName(), profile])