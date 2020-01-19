import json
import chatbot
import message
import firebasehelper
import httphelper

def parsePost(s:str,chatbots:dict,cred:tuple, orgId:int, botId:str)->None:
    jObject=json.loads(s)
    chatId=jObject['message']['chatId']
    msg=jObject['message']['message']
    if(jObject['message']['userId']==botId):
        return
    if(firebasehelper.getData(chatId)=='null'):
        cred = tuple(chatId) + cred + tuple(jObject['message']['userId'])
        res=chatbot.initialize(*cred)
    response = chatbots.parseString(chatId,msg)
    accessToken = firebasehelper.getDict(chatId)['accessToken']
    message.sendMessage(accessToken,chatId,orgId,response)
