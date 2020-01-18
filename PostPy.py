import requests


def sendPost(auth='e25772d080a0dc1206b421d1d20727e23f321ce3'):

    auth = auth
    url = "https://api-prod.hypercare.com/graphql/private"

    payload = "{\"query\":\"mutation SendPage($userId: ID!, $address: String!, $message: String!) {\\n"+\
    "    self {\\n"+\
    "        sms(userId: $userId, address: $address, message: $message)\\n"+\
    "    }\\n"+\
    "}\",\"variables\":{\"userId\":\"ae02888e-88b0-48a1-8712-d2464e27d288\",\"address\":\"+16476784076\",\"message\":\"Callback number: 1234\"}}"
    headers = {
      'hypercare-scope': 'lkajsldkjf98729834',
      'Content-Type': 'application/json',
      'Authorization': 'Bearer '+auth
    }

    response = requests.post(url, headers=headers, data=payload)
    
    print(response.status_code)
    print(response.text.encode('utf8'))


if __name__ == '__main__':

    sendPost()
