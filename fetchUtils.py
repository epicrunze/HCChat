import authentication
import requests
import json
from fuzzywuzzy import process
import message

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

def newChat(userIds, string, accessToken, hypercareScope, orgId):
    url = "https://api-prod.hypercare.com/graphql/private"
    payload = "{\"query\":\"mutation createChat($memberIds: [ID!]!, $title: String) {\\r\\n    createChat(members: $memberIds, title: $title) {\\r\\n        ...ChatFragment\\r\\n    }\\r\\n}\\r\\n\\r\\nfragment ChatFragment on Chat {\\r\\n    id\\r\\n    title\\r\\n    members {\\r\\n        ...GeneralUserFragment\\r\\n    }\\r\\n    lastMessage {\\r\\n        ...MessageFragment\\r\\n    }\\r\\n    lastUnreadMessage {\\r\\n        ...MessageFragment\\r\\n    }\\r\\n    unreadPriorityMessages\\r\\n}\\r\\n\\r\\nfragment GeneralUserFragment on GeneralUser {\\r\\n    id\\r\\n    username\\r\\n    firstname\\r\\n    lastname\\r\\n}\\r\\n\\r\\nfragment MessageFragment on Message {\\r\\n    id\\r\\n    type\\r\\n    message\\r\\n    sender {\\r\\n        ...GeneralUserFragment\\r\\n    }\\r\\n    dateCreated\\r\\n}\",\"variables\":{\"memberIds\":" + str(userIds).replace("'", "\"") + "}}"
    headers = {
                'hypercare-scope': hypercareScope,
                'Content-Type': 'application/json',
                'Authorization': 'Bearer ' + accessToken
                }

    response = requests.request("POST", url, headers=headers, data = payload)
    print(json.loads(response.text))
    chatId = json.loads(response.text)['data']['createChat']['id']


    #sending message
    message.sendMessage(accessToken, chatId, orgId, string)

    payload = "{\"query\":\"mutation removeMember($chatId: ID!, $userId: ID!) {\\n    chat(chatId: $chatId) {\\n        admin {\\n            removeMember(userId: $userId) {\\n                ...ChatFragment\\n            }\\n        }\\n    }\\n}\\n\\nfragment ChatFragment on Chat {\\n    id\\n    title\\n    members {\\n        ...GeneralUserFragment\\n    }\\n    lastMessage {\\n        ...MessageFragment\\n    }\\n    lastUnreadMessage {\\n        ...MessageFragment\\n    }\\n    unreadPriorityMessages\\n}\\n\\nfragment GeneralUserFragment on GeneralUser {\\n    id\\n    username\\n    firstname\\n    lastname\\n}\\n\\nfragment MessageFragment on Message {\\n    id\\n    type\\n    message\\n    sender {\\n        ...GeneralUserFragment\\n    }\\n    dateCreated\\n}\",\"variables\":{\"chatId\":\"" + chatId + "\",\"userId\":\"" + userIds[2] + "\"}}"

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text

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
        return ("user", user2id[topUser[0]], topUser[0])
    else:
        return ("dept", dept2id[topDept[0]], topDept[0])

if __name__ == "__main__":
    userIds = ["57bdf0d7-88bd-47c1-9b20-5a71a959c6bf", "23a58200-58c0-49a4-b359-e40f0a47d4f7", "a1496581-3e34-4aab-bf9d-1b3af586d052"]
    string = "bruhhhh"
    accessToken = "3051afcee63e45a01abcf0beb41048b8c0ecd4b0"
    hypercareScope = "eyJvcmdhbml6YXRpb25JZCI6NzEsInN0YXR1cyI6ImFkbWluIn0K"
    orgId = 71
    print(newChat(userIds, string, accessToken, hypercareScope, orgId))
