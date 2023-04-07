import json
from flask import Flask, render_template, request, redirect, sessions
from flask_socketio import SocketIO, emit  # 导入socketio包

name_space = '/websocket'
app = Flask(__name__)
app.secret_key = 'jzw'
socketio = SocketIO(app)
client_query = []


@socketio.on('connect', namespace=name_space)  # 有客户端连接会触发该函数
def on_connect():
    # 建立连接 sid:连接对象ID
    client_id = request.sid
    client_query.append(client_id)
    # emit(event_name, broadcasted_data, broadcast=False, namespace=name_space, room=client_id)  #指定一个客户端发送消息
    # emit(event_name, broadcasted_data, broadcast=True, namespace=name_space)  #对name_space下的所有客户端发送消息
    print('有新连接,id=%s接加入, 当前连接数%d' % (client_id, len(client_query)))


@socketio.on('disconnect', namespace=name_space)  # 有客户端断开WebSocket会触发该函数
def on_disconnect():
    # 连接对象关闭 删除对象ID
    client_query.remove(request.sid)
    print('有连接,id=%s接退出, 当前连接数%d' % (request.sid, len(client_query)))


# on('消息订阅对象', '命名空间区分')
@socketio.on('message', namespace=name_space)
def on_message(message):
    """ 服务端接收消息 """
    print('从id=%s客户端中收到消息，内容如下:' % request.sid)
    print(message)
    emit('my_response_message', "我收到了你的信息", broadcast=False, namespace=name_space, room=client_id)  # 指定一个客户端发送消息
    # emit('my_response_message', broadcasted_data, broadcast=True, namespace=name_space)  #对name_space下的所有客户端发送消息


@app.route('/')  # 初始化页面
def a():
    return render_template("test.html")


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
    # app.run()
