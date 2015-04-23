class CAppliedProfilesDiffCalculator(object):

    def CalculateDiff(self, appliedProfilesSource, appliedProfilesTarget):
        newProfiles = {}
        unchangedProfiles = {}
        deletedProfiles = {}

        def AddProfiles(dictionary, element, profiles):
            if not hasattr(profiles, '__iter__'):
                profiles = [profiles]
            dictionary.setdefault(element, set()).update(profiles)

        def AddNewProfiles(element, profiles):
            AddProfiles(newProfiles, element, profiles)

        def AddUnchangedProfiles(element, profiles):
            AddProfiles(unchangedProfiles, element, profiles)

        def AddDeletedProfiles(element, profiles):
            AddProfiles(deletedProfiles, element, profiles)

        for element, previousProfiles in appliedProfilesSource.iteritems():
            if element not in appliedProfilesTarget:
                AddDeletedProfiles(element, previousProfiles)
            else:
                currentProfiles = appliedProfilesTarget[element]
                intersect = currentProfiles.intersection(previousProfiles)
                added = currentProfiles - intersect
                deleted = previousProfiles - intersect
                AddNewProfiles(element, added)
                AddUnchangedProfiles(element, intersect)
                AddDeletedProfiles(element, deleted)

        for element, currentProfiles in appliedProfilesTarget.iteritems():
            if element not in appliedProfilesSource:
                AddNewProfiles(element, currentProfiles)

        return newProfiles, unchangedProfiles, deletedProfiles