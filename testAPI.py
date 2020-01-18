import requests
import json
import re       


def getSymptoms(token):

    parameters = {'token': token,
                  'language': 'en-gb'}
    #headers = {'Authorization': 'Bearer '+token}

    res = requests.get('https://sandbox-healthservice.priaid.ch/symptoms',
                       params=parameters)

    strContent = res.content.decode('utf-8')
    print(strContent)
    dictContent = json.loads(strContent)
    
    directDict = {}
    for i in range(len(dictContent)):
        idNum, symp = dictContent[i].values()
        directDict[idNum] = symp
    
    print(len(directDict))
    return directDict

if __name__ == '__main__':

    token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImphbWVzLmxpYW5neXlAZ21haWwuY29tIiwicm9sZSI6IlVzZXIiLCJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9zaWQiOiI2MzE3IiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy92ZXJzaW9uIjoiMjAwIiwiaHR0cDovL2V4YW1wbGUub3JnL2NsYWltcy9saW1pdCI6Ijk5OTk5OTk5OSIsImh0dHA6Ly9leGFtcGxlLm9yZy9jbGFpbXMvbWVtYmVyc2hpcCI6IlByZW1pdW0iLCJodHRwOi8vZXhhbXBsZS5vcmcvY2xhaW1zL2xhbmd1YWdlIjoiZW4tZ2IiLCJodHRwOi8vc2NoZW1hcy5taWNyb3NvZnQuY29tL3dzLzIwMDgvMDYvaWRlbnRpdHkvY2xhaW1zL2V4cGlyYXRpb24iOiIyMDk5LTEyLTMxIiwiaHR0cDovL2V4YW1wbGUub3JnL2NsYWltcy9tZW1iZXJzaGlwc3RhcnQiOiIyMDIwLTAxLTE4IiwiaXNzIjoiaHR0cHM6Ly9zYW5kYm94LWF1dGhzZXJ2aWNlLnByaWFpZC5jaCIsImF1ZCI6Imh0dHBzOi8vaGVhbHRoc2VydmljZS5wcmlhaWQuY2giLCJleHAiOjE1NzkzNjQ4MzMsIm5iZiI6MTU3OTM1NzYzM30.SwXGlwYv7EMYFft3NxvQVUw-Z26W3-zqI5ikyB-7drI'
    getSymptoms(token)
