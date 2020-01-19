import authentication
username = "ryanzhang"
password = "pass@word"
clientId = "uofthacksteam2"
clientSecret = "Lu7qXWP3b3d3"

print(authentication.getId(authentication.getAuthKey(username, password, clientId, clientSecret)[0], orgId=71))