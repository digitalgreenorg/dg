__author__ = 'Lokesh'

from configuration import tableDictionary, whereDictionary, selectDictionary, groupbyDictionary, categoryDictionary, orderDictionary, headerDictionary,checkValueSpecial

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
    valueSpecialToUse =  checkValueSpecial
    def __init__(self, user_input):
        self.user_input = user_input

    def initializeSelectDict(self):
        self.selectDictionaryToUse = selectDictionary
        #if self.user_input['value']['numAdoption'] == True and self.user_input['partition']['animator'] == True:
        #    self.selectDictionaryToUse['numAdoption']['count(person_id)'] = False
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

    def initializeValueSpecial(self):
        self.valueSpecialToUse = checkValueSpecial
        return checkValueSpecial