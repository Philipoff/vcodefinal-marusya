from __future__ import unicode_literals

from flask import Flask, request
from flask_cors import CORS

import json
import snake

app = Flask(__name__)
app.debug = True
CORS(app)


@app.route('/')
def index():
    return f'<h1>{"https" + request.base_url[4:]}forty/webhook</h1>'


@app.route('/marusya', methods=['POST', 'GET'])
def marusya():
    return "Marusya"


users_information = {}


@app.route('/forty/webhook', methods=['POST'])
def webhook():
    text = ''
    buttons = []
    # image_id = 0
    user_id = request.json["session"]["user_id"]
    message = request.json['request']['original_utterance'].lower().split()
    try:
        users_information[user_id]["score"]
    except KeyError as user_not_in_db_error:
        users_information[user_id] = {"score": 0, "matrix": snake.create_matrix(), "body": [(5, 5), (5, 6)]}
    if message[0] == 'старт':
        text = f"Запущена игра 'Змейка'!\n" \
               f"Управляйте змейкой командами влево\вправо\вниз\вверх, удачи!\n"
        users_information[user_id] = {"score": 0, "matrix": snake.create_matrix(), "body": [(5, 5), (5, 6)]}
        text += f"Счёт: {users_information[user_id]['score']}\n"
    else:
        if ' '.join(message) in ["влево", "вправо", "вниз", "вверх", "начать заново"]:
            exit_flag = False
            if message == ["начать", "заново"]:
                text = f"Запущена игра 'Змейка'!\n" \
                       f"Управляйте змейкой на кнопки, удачи!\n"
                users_information[user_id] = {"score": 0, "matrix": snake.create_matrix(), "body": [(5, 5), (5, 6)]}
                exit_flag = True
            if not exit_flag:
                text = ""
                error = ""
                if message[0] == "влево":
                    users_information[user_id]["matrix"], users_information[user_id]["body"], users_information[user_id]["score"], error = snake.move_left(users_information[user_id]["matrix"], users_information[user_id]["body"], users_information[user_id]["score"])
                if message[0] == "вправо":
                    users_information[user_id]["matrix"], users_information[user_id]["body"], users_information[user_id]["score"], error = snake.move_right(users_information[user_id]["matrix"], users_information[user_id]["body"], users_information[user_id]["score"])
                if message[0] == "вниз":
                    users_information[user_id]["matrix"], users_information[user_id]["body"], users_information[user_id]["score"], error = snake.move_down(users_information[user_id]["matrix"], users_information[user_id]["body"], users_information[user_id]["score"])
                if message[0] == "вверх":
                    users_information[user_id]["matrix"], users_information[user_id]["body"], users_information[user_id]["score"], error = snake.move_up(users_information[user_id]["matrix"], users_information[user_id]["body"], users_information[user_id]["score"])
                if error:
                    if error == "Lose":
                        text = "Змейка откусила себе хвост. Попробуйте ещё.\n" \
                               "Пересоздаю карту...\n"
                    else:
                        text = "Удивительно, но змейка вывернулась наизнанку. Попробуйте ещё.\n" \
                               "Пересоздаю карту...\n"
                    users_information[user_id] = {"score": 0, "matrix": snake.create_matrix(), "body": [(5, 5), (5, 6)]}
                text += f"Счёт: {users_information[user_id]['score']}\n"
        else:
            text = "Неверная команда! Используюте кнопки влево/вправо/вниз/вверх\n"
    text_matrix = ""
    for row in users_information[user_id]["matrix"]:
        text_matrix += ''.join([str(i) for i in row]) + '\n'
    text_matrix = text_matrix.replace('0', '~')
    text_matrix = text_matrix.replace('1', '9')
    text_matrix = text_matrix.replace('2', 'O')
    text_matrix = text_matrix.replace('3', 'H')
    text += text_matrix

    btn_left = {
        "title": "Влево",
    }
    btn_right = {
        "title": "Вправо",
    }
    btn_down = {
        "title": "Вниз",
    }
    btn_up = {
        "title": "Вверх",
    }
    [buttons.append(btn) for btn in [btn_left, btn_right, btn_down, btn_up]]
    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False,
            "text": text,
            "buttons": buttons
        }
    }

    return json.dumps(response, indent=2)


if __name__ == '__main__':
    app.run(port=3000)
