from flask import Flask, render_template, json, request
import pdb
import os
from Socket import Socket, ETHERNET_IP, WIFI_IP

app = Flask(__name__,static_url_path='')

S = Socket(ip="192.168.4.19")

@app.route('/<path:path>/css')
def send_js(path):
    return send_from_directory('css', path)

@app.route('/<path:path>/js')
def send_css(path):
    return send_from_directory('js', path)

@app.route('/hello')
def hello_world():
   return 'hello world'

@app.route('/')
def main():
    return render_template('index.html')


@app.route('/data', methods = ['POST'])
def data():
    data= request.get_json()
    print(data)
    S.send(data)
    result = {}
    return(json.dumps(result))

if __name__ == '__main__':
    app.run()
