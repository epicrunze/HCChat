import json
import chatbot
import message

def parsePost(s:str,chatbots:dict,cred:tuple, orgId:int):
    jObject=json.loads(s)
    chatId=jObject['message']['chatId']
    message=jObject['message']['message']
    if(chatId not in chatbots):
        chatbots[chatId]=chatbot.Chatbot(*cred)
    response = chatbots[chatId].parseString(message)
    messagesendMessage(chatbot.accessToken,chatId,orgId,response)
