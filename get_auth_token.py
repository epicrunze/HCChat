import requests

url = 'https://api-prod.hypercare.com/oauth/token'

header = {'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic ZGVtb2NsaWVudDpkZW1vY2xpZW50c2VjcmV0'}
body = {'grant_type' : 'password',
        'username': 'ryanzhang',
        'password': 'pass@word'}

response = requests.post(url, data=body, headers=header)

print(response.json()['response']['accessToken'])