import webhook
import authentication
import postParser
import httphelper
from flask import Flask, render_template, request

# Important values
WEBHOOK_URL="https://hyperchat.appspot.com/webhook"
AUTH_KEY=""
AUTH_EXPIRY=""
BOT_ID=""
CHATBOT_DICT={}
CREDENTIALS=('chatbot','chat@bot','uofthacksteam2','Lu7qXWP3b3d3')
ORG_ID=71

# Init Flask
app = Flask(__name__)
# Get the AUTH_KEY for the chat bot
AUTH_KEY,AUTH_EXIPRY=authentication.getAuthKey(*CREDENTIALS)
# Unlink any previous webhooks in place
webhook.removeWebhook(AUTH_KEY)
# Re-link the web app 
webhook.addWebhook(WEBHOOK_URL, AUTH_KEY)
# Obtain BOT_ID
BOT_ID=authentication.getId(AUTH_KEY,ORG_ID)

@app.route('/')# Root index for later :)
def root():
    return render_template('index.html')
    

@app.route('/webhook', methods=['POST']) # Allow only POST requests
def messageReceived():
    if request.method != 'POST':# Something went terribly wrong
        raise RuntimeError('A non-POST request was revieved by this function')
    postParser.parsePost(request.data,CHATBOT_DICT,CREDENTIALS,ORG_ID,BOT_ID)
    return 'OK.'
    


if __name__ == '__main__':
    #Debuging locally
    app.run(port=8080, debug=False)
