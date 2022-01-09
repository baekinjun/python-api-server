from datetime import datetime
import eventlet
from flask import Flask
from flask_socketio import SocketIO, emit, join_room

from postgredb import insert_pg
from common import check_datetime, insert_chat_box, chat_box_list

eventlet.monkey_patch()
chat = Flask(__name__)

socketio = SocketIO(chat, cors_allowed_origins='*', logger=True, engineio_logger=True)


@socketio.on('join_room')
def on_join(data):
    room = data['room']
    join_room(room)

    r_data = dict()
    r_data['time'] = str(datetime.strptime(str(str(datetime.now()))[0:10], '%Y-%m-%d'))[0:10]
    r_data['chat'] = check_datetime(list(chat_box_list[room]))
    emit('open_room', r_data, broadcast=True, to=room, room=room)


@socketio.on('leave_room')
def leave_room():
    leave_room('kr')
    leave_room('jp')
    leave_room('en')


@socketio.on('send_message')
def on_chat_sent(data):
    room = data['room']
    data['real_time'] = str(datetime.strptime(str(str(datetime.now()))[0:18], '%Y-%m-%d %H:%M:%S'))
    data['time'] = str(data['real_time'])[11:16]
    emit("message_sent", data, to=room, room=room)

    insert_chat_box(room, data)


if __name__ == "__main__":
    socketio.run(chat)
