import json
import chatbot
import message
import firebasehelper
import httphelper

def parsePost(s:str, orgId:int, botId:str)->None:
    jObject=json.loads(s)
    chatId=jObject['message']['chatId']
    msg=jObject['message']['message']
    if(jObject['message']['userId']==botId):
        return
    if(firebasehelper.getData(chatId)=='null'):
        res=chatbot.initialize(chatId,'chatbot','chat@bot','uofthacksteam2','Lu7qXWP3b3d3',jObject['message']['userId'])
    response = chatbot.parseString(chatId,msg)
    accessToken = firebasehelper.getDict(chatId)['accessToken']
    message.sendMessage(accessToken,chatId,orgId,response)
