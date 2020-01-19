from datetime import date
import httphelper

URL='https://hyperbase-f0472.firebaseio.com/users/'

def writeData(chatId:str)->None:
    data='{"'+chatId+'":"'+str(date.today())+'"}'
    header={'content-type':'application/json'}
    return httphelper.patch(URL+'.json',header,data)

def hasChatId(chatId:str)->bool:
    header={'content-type':'application/json'}
    return httphelper.get(URL+chatId+'.json',header).text!='null'
