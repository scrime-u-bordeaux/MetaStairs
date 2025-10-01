def promptWithDefaultValue(defaultValue, valueList, text):
    if defaultValue in valueList:
        return defaultValue
    else:
        print(text)
        for i, v in enumerate(valueList):
            print('{index} : {value}'.format(index = i + 1, value = v))
        choice = int(input('> ')) - 1
        return valueList[max(min(len(valueList) - 1, choice), 0)]
        