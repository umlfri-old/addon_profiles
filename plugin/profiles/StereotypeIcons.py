stereotypeIconFileMappings = {}


def CreateIconFileMapping(name, filename):
    stereotypeIconFileMappings[name] = 'icons/{0}'.format(filename)


CreateIconFileMapping('Actor', 'actor_image.png')
CreateIconFileMapping('Wizard', 'wizard.png')
CreateIconFileMapping('Map Location', 'maps_location.png')
CreateIconFileMapping('Loading', 'loading.png')
CreateIconFileMapping('Question Mark', 'question_mark.png')
CreateIconFileMapping('Settings', 'settings.png')