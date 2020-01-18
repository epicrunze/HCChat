import httphelper

def addWebhook(hook:str,auth:str)->str:
    url = "https://api-prod.hypercare.com/graphql/private"

    payload = "{\"query\":\"mutation RegisterWebhook($url: String!) {\\n    self {\\n        registerWebhook(url: $url) {\\n            url\\n            createdAt\\n            updatedAt\\n        }\\n    }\\n}\",\"variables\":{\"url\":\""+hook+"\"}}"
    headers = {
    'Content-Type': 'application/json',
    'Authorization':'Bearer '+auth
    }

    return httphelper.post(url,headers,payload).text.encode('utf8')

def removeWebhook(auth)->str:
    url = "https://api-prod.hypercare.com/graphql/private"
    
    payload = "{\"query\":\"mutation UnregisterWebhook {\\n    self {\\n        unregisterWebhook\\n    }\\n}\",\"variables\":{}}"
    headers = {
      'Content-Type': 'application/json',
      'Authorization':'Bearer '+auth
    }
    
    return httphelper.post(url,headers,payload).text.encode('utf8')
