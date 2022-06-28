#$env:FLASK_ENV = "development"
import math
import os
import time

from flask import Flask, render_template, request, json
import mimetypes
mimetypes.init()
mimetypes.add_type('application/javascript', '.mjs')
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', '.css')
app = Flask(__name__)
newestMessage = {}

@app.route('/', methods=['GET'])
def main():
    return render_template('./index.html')


@app.route('/poll', methods=['POST'])
def poll():
    requestData = json.loads(request.data)
    print(requestData)
    print(newestMessage)
    print(requestData == newestMessage)
    requestTime = math.ceil(time.time())*1000
    pollBreak = requestTime + 1000*10
    while requestData == newestMessage:
        time.sleep(0.01)
        if pollBreak < math.ceil(time.time())*1000:
            return {'msg': False}
    return {'msg': newestMessage}

@app.route('/printMessage', methods=['POST'])
def printMessage():
    global newestMessage
    requestData = json.loads(request.data)
    print(requestData)
    counter = 0
    for x in time.ctime((time.time())):
        if x == ":":
            requestData["time"]=time.ctime((time.time()))[counter-2:counter+6]
            break
        counter = counter+1
    newestMessage = requestData
    return {}

@app.route('/getLatest', methods=['POST'])
def getLatest():
    return {'huizong': newestMessage}

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port, threaded=True)
