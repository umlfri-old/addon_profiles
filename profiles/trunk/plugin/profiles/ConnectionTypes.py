class KnownConnectionTypes:
    ExtensionType = 'Extension'

    @classmethod
    def IsExtension(cls, connection):
        return connection.type.name == cls.ExtensionType