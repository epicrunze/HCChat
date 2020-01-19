from datetime import date
import httphelper

URL='https://hyperbase-f0472.firebaseio.com/'

def writeData(data:dict,ext:str='')->None:
    data=str(data)
    header={'content-type':'application/json'}
    return httphelper.patch(URL+ext+'.json',header,data)

def getData(chatId:str,ext:str='')->str:
    header={'content-type':'application/json'}
    return httphelper.get(URL+ext+chatId+'.json',header).text
