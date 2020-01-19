from datetime import date
import httphelper
import json

URL='https://hyperbase-f0472.firebaseio.com/'

def writeData(data:dict,ext:str='chatbot/'):
    data=str(data).replace("'", '\"')
    header={'content-type':'application/json'}
    return httphelper.patch(URL+ext+'.json',header,data)

def getData(chatId:str,ext:str='chatbot/')->str:
    header={'content-type':'application/json'}
    return httphelper.get(URL+ext+chatId+'.json',header).text

def json2Dict(string):
    return json.loads(string)

def getDict(chatId, ext='chatbot/'):
    return json2Dict(getData(chatId, ext))

def writeDict(data, chatId, ext='chatbot/'):
    return writeData({str(chatId): data})