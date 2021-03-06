import os
from imports.gtk2 import gtk, gobject
from SelectProfilesDialog import CSelectProfilesDialog
from ..ElementTypes import KnownElementTypes
from OrphanedProfileApplicationDeletionConfirmation import COrphanedProfileApplicationDeletionConfirmation
from util import FixTreeViewSelectionOnRightClick


class CProfileListDialog(object):

    gladeFile = os.path.join(os.path.dirname(__file__), "profileListDialog.glade")

    def __init__(self, projectRoot, appliedProfiles, availableProfiles, orphanedProfileApplications=None):
        self.projectRoot = projectRoot
        self.availableProfiles = availableProfiles

        self.wTree = gtk.Builder()
        self.wTree.add_from_file(self.gladeFile)

        signals = {
            'tvProfiles_button_press_event': self.tvProfiles_button_press_event_handler,
            'addProfileMenuItem_activate_event': self.addProfileMenuItem_activate_event_handler,
            'removeProfileMenuItem_activate_event': self.removeProfileMenuItem_activate_event_handler,
            'profileListDialog_show_event': self.profileListDialog_show_event_handler,
        }

        self.wTree.connect_signals(signals)

        self.__projectTreeStore = gtk.TreeStore(str, str, object)
        self.__tvProjectTree = self.wTree.get_object('tvProjectTree')
        self.__tvProjectTree.set_model(self.__projectTreeStore)
        self.__tvProjectTree.get_selection().connect('changed', self.tvProjectTree_selection_changed_handler)

        self.__dialog = self.wTree.get_object('profileListDialog')
        self.__tvProfiles = self.wTree.get_object('tvProfiles')
        self.__profileListStore = gtk.ListStore(str, object)
        self.__tvProfiles.set_model(self.__profileListStore)
        self.__profileList = self.__tvProfiles.get_model()
        self.__profileList.clear()
        self.__profileListPopupMenu = self.wTree.get_object('profileListPopupMenu')
        self.__removeProfileMenuItem = self.wTree.get_object('removeProfileMenuItem')

        self.__packageProfiles = appliedProfiles
        self.__orphanedProfileApplications = orphanedProfileApplications

    def Show(self):
        self.__FillProjectTree()

        result = self.__dialog.run()
        self.__dialog.hide()
        return result == 0

    def __FillProjectTree(self):
        self.__projectTreeStore.clear()
        self.__FillProjectTreeInternal(self.projectRoot, None)

    def __FillProjectTreeInternal(self, root, parent):
        parent = self.__projectTreeStore.append(parent)
        self.__projectTreeStore.set(parent, 0, root.name, 1, root.type.name, 2, root)

        for element in root.children:
            self.__FillProjectTreeInternal(element, parent)

    def __FillProfiles(self, element):
        self.__ClearProfileList()

        profiles = self.__packageProfiles.get(element, [])

        for profile in profiles:
            self.__profileList.append([profile.GetName(), profile])

    def __ClearProfileList(self):
        self.__profileListStore.clear()

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

    def __GetSelectedProjectElement(self):
        iter = self.__tvProjectTree.get_selection().get_selected()[1]
        if iter is None:
            return None
        element, = self.__projectTreeStore.get(iter, 2)
        return element

    def tvProjectTree_selection_changed_handler(self, widget):
        element = self.__GetSelectedProjectElement()
        if element is not None:
            isPackage = KnownElementTypes.IsPackage(element)
            self.__tvProfiles.set_sensitive(isPackage)
            if isPackage:
                self.__FillProfiles(element)
            else:
                self.__ClearProfileList()

    def addProfileMenuItem_activate_event_handler(self, widget):
        packageElement = self.__GetSelectedProjectElement()

        profile = CSelectProfilesDialog().ChooseProfile(self.availableProfiles)
        if profile is None:
            return

        self.__AddProfiles(packageElement, [profile])

    def __AddProfiles(self, package, profiles):
        self.__GetPackageProfiles(package).update(profiles)
        self.__FillProfiles(package)

    def removeProfileMenuItem_activate_event_handler(self, widget):
        iter = self.__tvProfiles.get_selection().get_selected()[1]
        if iter is None:
            return None
        profile, = self.__profileListStore.get(iter, 1)
        self.__profileListStore.remove(iter)
        self.__GetPackageProfiles().remove(profile)

    def __GetPackageProfiles(self, package=None):
        if package is None:
            package = self.__GetSelectedProjectElement()

        return self.__packageProfiles.setdefault(package, set())

    def profileListDialog_show_event_handler(self, widget):
        if self.__orphanedProfileApplications is not None and len(self.__orphanedProfileApplications) > 0:
            self.__DisplayWarningForOrphanedProfiles(self.__orphanedProfileApplications)
            self.__orphanedProfileApplications = None

    def __DisplayWarningForOrphanedProfiles(self, orphanedProfileApplications):
        confirmation = COrphanedProfileApplicationDeletionConfirmation(orphanedProfileApplications, self.__dialog)
        if confirmation.GetConfirmation() == True:
            self.__RemoveOrphanedApplications(orphanedProfileApplications)
        else:
            gobject.timeout_add(15, lambda: self.__dialog.response(1))

    def __RemoveOrphanedApplications(self, orphanedProfileApplications):
        for package, profileApplications in orphanedProfileApplications.iteritems():
            for orphanedProfileApplication in profileApplications:
                self.__GetPackageProfiles(package).remove(orphanedProfileApplication)
