import httphelper

def getAuthKey(username:str, password:str, clientId:str, clientSecret:str)->str:

    url = 'https://api-prod.hypercare.com/oauth/token'

    authEncoded=httphelper.encodeBase64(clientId+':'+clientSecret)

    headers = {'Content-Type': 'application/x-www-form-urlencoded',
               'Authorization': 'Basic '+authEncoded}
    payload = {'grant_type' : 'password',
        'username': username,
        'password': password}
    
    response = httphelper.post(url,headers,payload).json()
    return (response['response']['accessToken'],response['response']['accessTokenExpiresAt'])

def getId(auth:str, orgId:int):
    
    url = "https://api-prod.hypercare.com/graphql/private"
    hypercareScope=httphelper.encodeBase64('{"organizationId":'+str(orgId)+'}')

    payload = "{\"query\":\"query self {\\n    me {\\n        ...FullUserFields\\n    }\\n}\\n\\nfragment FullUserFields on FullUser {\\n    id\\n    firstname\\n    lastname\\n    username\\n    role\\n    profilePic {\\n        url\\n    }\\n    inviteCode\\n}\",\"variables\":{}}"
    headers = {
      'hypercare-scope': hypercareScope,
      'Content-Type': 'application/json',
      'Authorization':'Bearer '+auth
    }

    response = httphelper.post(url, headers, payload).json()
    return response['data']['me']['id']
