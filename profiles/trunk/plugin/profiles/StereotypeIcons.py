stereotypeIconFileMappings = {}


def CreateIconFileMapping(name, filename):
    stereotypeIconFileMappings[name] = 'icons/{0}'.format(filename)


CreateIconFileMapping('Actor', 'actor_image.png')