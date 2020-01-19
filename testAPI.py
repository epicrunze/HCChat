import requests
import json
import re       

def getSymptoms(token):

    parameters = {'token': token,
                  'language': 'en-gb'}
    # headers = {'Authorization': 'Bearer '+token}

    res = requests.get('https://sandbox-healthservice.priaid.ch/symptoms',
                       params=parameters)

    strContent = res.content.decode('utf-8')
    # print(strContent)
    dictContent = json.loads(strContent)

    directDict = {}
    for i in range(len(dictContent)):
        try:
            idNum, symp = dictContent[i].values()
            symp = symp.lower()
            directDict[idNum] = symp
        except AttributeError:
            raise Exception("Refresh Authentication Token")

    return directDict


def getDiagnosis(token, symId='[9,10,11]', gender='male', year_of_birth='1998'):

    parameters = {'token': token,
                  'language': 'en-gb',
                  'symptoms': symId,
                  'gender': gender,
                  'year_of_birth': year_of_birth}

    res = requests.get('https://sandbox-healthservice.priaid.ch/diagnosis',
                       params=parameters)
    
    res.raise_for_status()
    strContent = res.content.decode('utf-8')
    dictContent = json.loads(strContent) #  Retrieve immediate list
    if len(dictContent) != 0:
        dictContent = dictContent[0]
    return dictContent
