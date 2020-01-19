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
    if(chatId not in chatbots):
        if(firebasehelper.hasChatId(chatId)):
            httphelper.post('localhost/webhook',{},s)
        else:
            cred += tuple(chatId) + tuple(jObject['message']['userId'])
            chatbots[chatId]=chatbot.Chatbot(*cred)
            firebaseHelper.writeData(chatId)
    response = chatbots[chatId].parseString(msg)
    message.sendMessage(chatbots[chatId].accessToken,chatId,orgId,response)
