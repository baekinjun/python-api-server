from collections import deque
from datetime import datetime

chat_box_list = {
    'kr': deque(),
    'jp': deque(),
    'en': deque()
}


def check_datetime(data):
    TODAY = datetime.strptime(str(datetime.now())[0:10], '%Y-%m-%d')
    for check in data:
        check_time = datetime.strptime(check['real_time'][0:10], '%Y-%m-%d')
        if check_time != TODAY:
            check['time'] = str(check['real_time'])[5:16]
    return data


def insert_chat_box(room, data):
    chat_box = chat_box_list[room]
    if len(chat_box) > 30:
        chat_box.popleft()
        chat_box.append(data)
    else:
        chat_box.append(data)
