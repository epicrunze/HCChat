import authentication
import requests
import json

def fetchUsers(hypercareScope = 'eyJvcmdhbml6YXRpb25JZCI6NzEsInN0YXR1cyI6ImFkbWluIn0K', username = "chatbot", password="chat@bot", clientId="uofthacksteam2", clientSecret="Lu7qXWP3b3d3"):
    url = "https://api-prod.hypercare.com/graphql/private"
    auth = authentication.getAuthKey(username, password, clientId, clientSecret)
    headers = {'hypercare-scope': hypercareScope, 'Content-Type': 'application/json', "Authorization": 'Bearer ' + auth[0]}
    payload = "{\"query\":\"query fetchColleagues {\\n    colleagues {\\n        ...GeneralUserFragment\\n    }\\n}\\n\\nfragment GeneralUserFragment on GeneralUser {\\n    id\\n    firstname\\n    lastname\\n    role\\n     status\\n}\",\"variables\":{}}"

    response = requests.request('POST', url, headers=headers, data=payload)

    return json.loads(response.text)['data']['colleagues']

if __name__ == "__main__":
    print(fetchUsers())