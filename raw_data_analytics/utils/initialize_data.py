__author__ = 'Lokesh'

from configuration import tableDictionary, whereDictionary, selectDictionary, groupbyDictionary, categoryDictionary, orderDictionary, headerDictionary

class initialize_library():
    Dict = {}
    lookup_matrix = {}
    idElementKey = ''
    idElementValue = -1
    tableDictionaryToUse = tableDictionary
    whereDictionaryToUse = whereDictionary
    selectDictionaryToUse = selectDictionary
    groupbyDictionaryToUse = groupbyDictionary
    categoryDictionaryToUse = categoryDictionary
    orderDictionaryToUse = orderDictionary
    headerDictionaryToUse = headerDictionary

    def initializeSelectDict(self,user_input):
        self.selectDictionaryToUse = selectDictionary
        return self.selectDictionaryToUse

    def initializeWhereDict(self):
        self.whereDictionaryToUse = whereDictionary
        return self.whereDictionaryToUse

    def initializeTableDict(self):
        self.tableDictionaryToUse = tableDictionary
        return self.tableDictionaryToUse;

    def initializeGroupByDict(self):
        self.groupbyDictionaryToUse = groupbyDictionary
        return self.groupbyDictionaryToUse

    def initializeCategoryDict(self):
        self.categoryDictionaryToUse = categoryDictionary
        return self.categoryDictionaryToUse

    def initializeOrderDict(self):
        self.orderDictionaryToUse = orderDictionary
        return self.orderDictionaryToUse

    def initializeHeaderDict(self):
        self.headerDictionaryToUse = headerDictionary
        return headerDictionary