import json
import chatbot
import message

f = open('chats.dat','a')

def parsePost(s:str,chatbots:dict,cred:tuple, orgId:int, botId:str):
    jObject=json.loads(s)
    chatId=jObject['message']['chatId']
    msg=jObject['message']['message']
    if(jObject['message']['userId']==botId):
        return
    if(chatId not in chatbots):
        chatbots[chatId]=chatbot.Chatbot(*cred)
        f.write(chatId+'\n')
        f.flush()
    response = chatbots[chatId].parseString(msg)
    message.sendMessage(chatbots[chatId].accessToken,chatId,orgId,response)
