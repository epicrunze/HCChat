from datetime import date
from firebase import firebase

firebase = firebase.FirebaseApplication('https://hyperbase-f0472.firebaseio.com/', None)

def writeData(chatId:str)->None:
    data={chatId:'time'}
    res=firebase.patch('/users/',date.today())
    print(res)

def hasChatId(chatId:str)->bool:
    return firebase.get('/users/',chatId)!=None
