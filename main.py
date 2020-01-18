import webhook
from flask import Flask, render_template, request

app = Flask(__name__)


WEBHOOK_URL="https://praxis-atrium-265504.appspot.com/test-post"

@app.route('/')# Root index for later :)
def root():
    return render_template('index.html')
    

@app.route('/test-post', methods=['POST']) #allow only POST requests
def messageReceived():
    if request.method != 'POST':# Something went terribly wrong
        raise RuntimeError('A non-POST request was revieved by this function')
    #Put code here to handle messages
    


if __name__ == '__main__':
    #Debuging locally
    app.run(host='127.0.0.1', port=8080, debug=True)
