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
