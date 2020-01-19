from spellchecker import SpellChecker
from ELMoForManyLangs.elmoformanylangs import Embedder
import numpy as np
from testAPI import getSymptoms, getDiagnosis



def softmax(x):
    num = np.exp(x-np.max(x))
    normF = num.sum()
    return num/normF


def reverseKey(cDict, value):
    for k in cDict.keys():
        if cDict[k] == value:
            return k
    raise Exception("Value not in Dict", value)


class SymptomRevision:

    def __init__(self, token):
        self.token = token
        self.spell = SpellChecker()
        self.wordEmbed = Embedder('./ELMoForManyLangs/144')
        self.symDict = getSymptoms(token)
        self.valid_sym = list(self.symDict.values())

        self.embeddingDict = {}
        for sym in self.valid_sym:
            fixedRep = self.wordEmbed.sents2elmo(sym)
            self.embeddingDict[sym] = fixedRep[0]

    def restrictWords(self, inputList):

        newList = []
        for w in inputList:
            word = self.restrictWord(w)
            if word is not None:
                newList.append(self.restrictWord(w))
        return newList

    def restrictWord(self, userInput):

        '''
        Procedure:
        - Validate input spelling
        - Test if in set of known vocabulary
        - If not, project into embedding space, take L2 distance between
          known symptoms and user symptom (similarity)
        - Select symptom with closest distance, pass to diagnosis
        '''

        thresh = .5
        splitString = userInput.split(' ')
        for i in range(len(splitString)):
            splitString[i] = self.spell.correction(splitString[i])
        userInput = ' '.join(splitString)
        userInput = userInput.lower()

        if userInput in self.valid_sym:
            return userInput

        delFlag = True
        rep = self.wordEmbed.sents2elmo(userInput)[0]

        distList = np.zeros((len(self.embeddingDict)))
        for i, v in enumerate(self.embeddingDict.values()):
            #  Use cosine similarity for similarity metric
            val = np.abs(np.squeeze(np.dot(rep, np.transpose(v)) /
                                    (np.linalg.norm(rep)*np.linalg.norm(v))))
            distList[i] = val
            if distList[i] < thresh:  # Threshold Value
                delFlag = False

        if delFlag is True:
            return None
        else:
            vocabSym = list(self.embeddingDict.keys())[np.argmax(distList)]
        return vocabSym

    def trackDiagnosis(self, symptomList, gender, birthYear):

        '''
        symptomList - list of symptoms (strings) - processed by restrictWord(s)
        gender - single string specifying gender
        birthYear - single integer/string specifying year of birth
        '''

        birthYear = str(birthYear)
        gender = gender.lower()
        currentSym = '[]'
        lastDiag = None
        currentDiag = None
        for i, v in enumerate(symptomList):
            #  Prep API request
            if i == 0:
                currentSym = currentSym[0]+str(reverseKey(self.symDict, v)) + \
                                                            currentSym[-1]
            else:
                currentSym = currentSym[:-2]+', ' + \
                                str(reverseKey(self.symDict, v))+currentSym[-1]
            if i == 1:
                lastDiag = currentDiag
            currentDiag = getDiagnosis(self.token, currentSym, gender,
                                       birthYear)
            if len(currentDiag) <= 1:
                #  Early return if combination of symptoms leads to failed
                #  diagnosis
                return lastDiag

        return currentDiag

token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImphbWVzLmxpYW5neXlAZ21haWwuY29tIiwicm9sZSI6IlVzZXIiLCJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9zaWQiOiI2MzE3IiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy92ZXJzaW9uIjoiMjAwIiwiaHR0cDovL2V4YW1wbGUub3JnL2NsYWltcy9saW1pdCI6Ijk5OTk5OTk5OSIsImh0dHA6Ly9leGFtcGxlLm9yZy9jbGFpbXMvbWVtYmVyc2hpcCI6IlByZW1pdW0iLCJodHRwOi8vZXhhbXBsZS5vcmcvY2xhaW1zL2xhbmd1YWdlIjoiZW4tZ2IiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL2V4cGlyYXRpb24iOiIyMDk5LTEyLTMxIiwiaHR0cDovL2V4YW1wbGUub3JnL2NsYWltcy9tZW1iZXJzaGlwc3RhcnQiOiIyMDIwLTAxLTE4IiwiaXNzIjoiaHR0cHM6Ly9zYW5kYm94LWF1dGhzZXJ2aWNlLnByaWFpZC5jaCIsImF1ZCI6Imh0dHBzOi8vaGVhbHRoc2VydmljZS5wcmlhaWQuY2giLCJleHAiOjE1Nzk0MzQwMjEsIm5iZiI6MTU3OTQyNjgyMX0.Lx7gNkA3EqD5-hi4_kX_k1tC1wM19MMYajMjOcBzrzI'
symRev = SymptomRevision(token)
