import requests

def post(url:str,headers:dict,payload:str):
    return requests.request("POST", url, headers=headers, data = payload)
