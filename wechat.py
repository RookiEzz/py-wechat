#coding=utf-8
import threading
import requests
import json
from flask import Flask, make_response
import itchat

qrSource = ''
KEY = 'f07131b709ad4568bb81c177dafc0f97'

def start_flask():
    flaskApp = Flask('itchat')
    @flaskApp.route('/')
    def return_qr():
        if len(qrSource) < 100:
            return qrSource
        else:
            response = make_response(qrSource)
            response.headers['Content-Type'] = 'image/jpeg'
            return response
    flaskApp.run(host='0.0.0.0')
flaskThread = threading.Thread(target=start_flask)
flaskThread.setDaemon(True)
flaskThread.start()

def get_response(msg):
    # 这里我们就像在“3. 实现最简单的与图灵机器人的交互”中做的一样
    # 构造了要发送给服务器的数据
    apiUrl = 'http://www.tuling123.com/openapi/api'
    data = {
        'key'    : KEY,
        'info'   : msg,
        'userid' : 'wechat-robot',
    }
    try:
        data = json.dumps(data)
        r = requests.post(apiUrl, data=data).json()
        print r
        # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
        return r.get('text')
    # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
    # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
    except:
        # 将会返回一个None
        return

def qrCallback(uuid, status, qrcode):
    if status == '0':
        global qrSource
        qrSource = qrcode
    elif status == '200':
        qrSource = 'Logged in!'
    elif status == '201':
        qrSource = 'Confirm'

@itchat.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
    # 为了保证在图灵Key出现问题的时候仍旧可以回复，这里设置一个默认回复
    defaultReply = '工作中'.decode('utf8')
    print msg['User']
    # 如果图灵Key出现问题，那么reply将会是None
    reply = get_response(msg['Text'])
    # a or b的意思是，如果a有内容，那么返回a，否则返回b
    # 有内容一般就是指非空或者非None，你可以用`if a: print('True')`来测试
    # 指定用户不回复消息
    if msg['FromUserName'] ==   '@7359012517be32edf8936a68e04a5191b96c581289de22d8489c37fb5963b542':
        return False
    else :
        return defaultReply

itchat.auto_login(True, qrCallback=qrCallback)
itchat.run()