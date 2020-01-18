import json

def parsePost(s:str):
    jObject=json.loads(s)
    print(jObject['message']['chatId'])
    print(jObject['message']['messages'])
