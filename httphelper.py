import requests
import base64

def post(url:str,headers:dict,payload:str):
    return requests.request("POST", url, headers=headers, data = payload)

def patch(url:str,headers:dict,payload:str):
    return requests.request("PATCH", url, headers=headers, data=payload)

def get(url:str,headers:dict):
    return requests.request("GET",url,headers=headers)

def encodeBase64(s:str)->str:
    encodedBytes = base64.b64encode(s.encode("utf-8"))
    return str(encodedBytes, "utf-8")
