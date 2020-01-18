import json
import chatbot

def parsePost(s:str,chatbots:dict,cred:tuple):
    jObject=json.loads(s)
    chatId=jObject['message']['chatId']
    message=jObject['message']['message']
    print(chatId)
    print(message)
    if(chatId not in chatbots):
        chatbots[chatId]=chatbot.Chatbot(*cred)
    print(chatbots[chatId].process)
    print(chatbots[chatId].parseString(message))
    print(chatbots[chatId].process)
    print('----------------')
    
