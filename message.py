import httphelper

def sendMessage(auth:str,chatId:str,orgId:int,message:str):
    if(message==None):
        return
    url = "https://api-prod.hypercare.com/graphql/private"
    hypercareScope=httphelper.encodeBase64('{"organizationId":'+str(orgId)+'}')

    payload = "{\"query\":\"mutation sendMessage($chatId: ID!, $message: String!, $fileId: Int, $type: MessageType, $priority: Boolean) {\\n"+\
    "    chat(chatId: $chatId) {\\n"+\
    "        sendMessage(message: $message, type: $type, fileId: $fileId, priority: $priority) {\\n"+\
    "            id\\n"+\
    "            image\\n"+\
    "            attachment {\\n"+\
    "                ...AttachmentFragment\\n"+\
    "            }\\n"+\
    "            message\\n"+\
    "            type\\n"+\
    "            sender {\\n"+\
    "                id\\n"+\
    "                username\\n"+\
    "            }\\n"+\
    "        }\\n"+\
    "    }\\n"+\
    "}\\n"+\
    "\\n"+\
    "fragment AttachmentFragment on Attachment {\\n"+\
    "    id\\n"+\
    "    url\\n"+\
    "    mimeType\\n"+\
    "    fileName\\n"+\
    "}\",\"variables\":{\"chatId\":\""+chatId+"\",\"message\":\""+message+"\",\"type\":\"text\",\"priority\":false}}"

    headers = {
    'hypercare-scope': hypercareScope,
    'Content-Type': 'application/json',
    'Authorization':'Bearer '+auth
    }

    response = httphelper.post(url, headers, payload)
    
    print(response.status_code)
    print(response.text.encode('utf8'))


