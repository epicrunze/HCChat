from datetime import date
import httphelper

URL='https://hyperbase-f0472.firebaseio.com/users/'

def writeData(data:dict)->None:
    data=str(data)
    header={'content-type':'application/json'}
    return httphelper.patch(URL+'.json',header,data)

def getData(chatId:str)->str:
    header={'content-type':'application/json'}
    return httphelper.get(URL+chatId+'.json',header).text
