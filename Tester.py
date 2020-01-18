import authentication
username = "chatbot"
password = "chat@bot"
clientId = "uofthacksteam2"
clientSecret = "Lu7qXWP3b3d3"

print(authentication.getAuthKey(username, password, clientId, clientSecret))