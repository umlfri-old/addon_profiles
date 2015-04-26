from imports.gtk2 import gtk

class COrphanedProfileApplicationDeletionConfirmation(object):

    __messageTextTemplate = "Warning! There are packages with profile applications for profiles, " \
                            "which does not exist in project anymore: \n\n{0}\n\n" \
                            "It is not possible to change applied profiles, when there are missing profiles." \
                            "These applications have to be removed. Do you want to continue?"

    def __init__(self, orphanedProfileApplications, parentWindow=None):
        self.__packageNames = '\n'.join((package.name for package in orphanedProfileApplications.keys()))
        self.__parentWindow=parentWindow

    def GetConfirmation(self):
        messageText = self.__messageTextTemplate.format(self.__packageNames)

        messageDialog = gtk.MessageDialog(self.__parentWindow, gtk.DIALOG_MODAL, gtk.MESSAGE_WARNING,
                                          gtk.BUTTONS_OK_CANCEL, messageText)
        response = messageDialog.run()
        messageDialog.destroy()
        return response == gtk.RESPONSE_OK