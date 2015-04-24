from ast import literal_eval


def AppendItemsIntoList(element, attributeID, items):
    for i in range(0, len(items)):
        element.append_item(attributeID)

    values = literal_eval(element.values[attributeID])
    for i, item in enumerate(items):
        index = len(values) - i - 1
        pathToItem = '{0}[{1}]'.format(attributeID, index)
        for key, value in item.iteritems():
            path = '{0}.{1}'.format(pathToItem, key)
            element.values[path] = value