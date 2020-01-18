import json
import chatbot
import message

def parsePost(s:str,chatbots:dict,cred:tuple, orgId:int, botId:str):
    jObject=json.loads(s)
    chatId=jObject['message']['chatId']
    msg=jObject['message']['message']
    if(jObject['message']['userId']==botId):
        return
    if(chatId not in chatbots):
        chatbots[chatId]=chatbot.Chatbot(*cred)
    response = str(chatbots[chatId].parseString(msg))+' - '+str(chatId)+' - '+str(id(chatbots[chatId]))
    message.sendMessage(chatbots[chatId].accessToken,chatId,orgId,response)
