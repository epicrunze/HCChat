import authentication
import requests
import json
import numpy as np
from fuzzywuzzy import process

def fetchUsers(deptId, hypercareScope = 'eyJvcmdhbml6YXRpb25JZCI6NzEsInN0YXR1cyI6ImFkbWluIn0K', username = "chatbot", password="chat@bot", clientId="uofthacksteam2", clientSecret="Lu7qXWP3b3d3"):
    '''returns list of dictionaries with attributes: id, firstname, lastname, role, status'''

    url = "https://api-prod.hypercare.com/graphql/private"
    auth = authentication.getAuthKey(username, password, clientId, clientSecret)
    headers = {'hypercare-scope': hypercareScope, 'Content-Type': 'application/json', "Authorization": 'Bearer ' + auth[0]}
    payload = "{\"query\":\"query fetchColleagues {\\n    colleagues {\\n        ...GeneralUserFragment\\n    }\\n}\\n\\nfragment GeneralUserFragment on GeneralUser {\\n    id\\n    firstname\\n    lastname\\n    role\\n     status\\n}\",\"variables\":{}}"

    response = requests.request('POST', url, headers=headers, data=payload)

    return json.loads(response.text)['data']['colleagues']

def fetchDepts(site=0, hypercareScope = 'eyJvcmdhbml6YXRpb25JZCI6NzEsInN0YXR1cyI6ImFkbWluIn0K', username = "chatbot", password="chat@bot", clientId="uofthacksteam2", clientSecret="Lu7qXWP3b3d3"):
    '''returns list of dicts with keys: id, name, image, createdAt, updatedAt'''

    url = "https://api-prod.hypercare.com/graphql/private"
    auth = authentication.getAuthKey(username, password, clientId, clientSecret)
    headers = {'hypercare-scope': hypercareScope, 'Content-Type': 'application/json', "Authorization": 'Bearer ' + auth[0]}
    payload = payload = "{\"query\":\"query fetchSites {\\n    locating {\\n        sites {\\n            ...SiteFragment\\n        }\\n    }\\n}\\n\\nfragment SiteFragment on Site { \\n    id\\n    name\\n    image\\n    departments {\\n        ...DepartmentFragment\\n    }\\n    createdAt\\n    updatedAt\\n}\\n\\nfragment DepartmentFragment on Department {\\n    id\\n    name\\n    image\\n    createdAt\\n    updatedAt\\n}\",\"variables\":{}}"

    response = requests.request('POST', url, headers=headers, data=payload)

    return json.loads(response.text)["data"]["locating"]["sites"][site]["departments"]

def fetchChat(userId, ):
    pass

def fetchName(string):
    '''returns a tuple of key, value, where keys can be "user" or "dept" and value is the id'''
    deptlist = fetchDepts()
    userlist = []
    for dept in deptlist:
        userlist += fetchUsers(int(dept["id"]))

    user2id = {"{} {}".format(x['firstname'], x['lastname']): x['id'] for x in userlist}
    dept2id = {x['name']: x['id'] for x in deptlist}

    topDept = process.extractOne(string, list(dept2id.keys()))
    topUser = process.extractOne(string, list(user2id.keys()))

    if topUser[1] > topDept[1]:
        return ("user", user2id[topUser[0]])
    else:
        return ("dept", dept2id[topUser[0]])

if __name__ == "__main__":
    print(fetchName("ryan zhang")) 
    