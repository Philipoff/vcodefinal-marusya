from __future__ import unicode_literals

from flask import Flask, request
from flask_cors import CORS

import json
import logic

app = Flask(__name__)
app.debug = True
CORS(app)


@app.route('/')
def index():
    return '<h1>Webhook URL = https://127.0.0.1:3000/webhook</h1>'


@app.route('/marusya', methods=['POST', 'GET'])
def marusya():
    return "Marusya"


users_information = {}


@app.route('/webhook', methods=['POST'])
def webhook():
    text = ''
    buttons = []
    # image_id = 0
    user_id = request.json["session"]["user_id"]
    message = request.json['request']['original_utterance'].lower().split()
    try:
        users_information[user_id]["score"]
    except KeyError as user_not_in_db_error:
        users_information[user_id] = {"score": 0, "last_item": ""}
    if message[0] == 'старт':
        text = f"Запущена игра '2048'!\n" \
               f"Управляйте игрой командами влево\вправо\вниз\вверх, удачи!\n"
        users_information[user_id] = {"score": 0, "matrix": logic.create_matrix()}
        users_information[user_id]["matrix"] = logic.generate_new_num(users_information[user_id]["matrix"])
        # image_id = logic.make_image(users_information[user_id]["matrix"], user_id)
        text += f"Счёт: {users_information[user_id]['score']}"
    else:
        if ' '.join(message) in ["влево", "вправо", "вниз", "вверх", "начать заново"]:
            exit_flag = False
            if message == ["начать", "заново"]:
                text = f"Запущена игра '2048'!\n" \
                       f"Управляйте игрой на кнопки, удачи!\n"
                users_information[user_id] = {"score": 0, "matrix": logic.create_matrix()}
                users_information[user_id]["matrix"] = logic.generate_new_num(users_information[user_id]["matrix"])
                exit_flag = True
            if not exit_flag:
                start_matrix = users_information[user_id]["matrix"][:][:]
                users_information[user_id]["matrix"], users_information[user_id]["score"] = logic.swipe(
                    users_information[user_id]["matrix"][:][:], message[0], users_information[user_id]["score"])
                # image_id = logic.make_image(users_information[user_id]["matrix"], user_id)
                text += f"Счёт: {users_information[user_id]['score']}"
                if start_matrix != users_information[user_id]["matrix"]:
                    users_information[user_id]["matrix"] = logic.generate_new_num(users_information[user_id]["matrix"])
                if logic.is_move_is_impossible(users_information[user_id]["matrix"][:][:], -1):
                    text = f"К сожалению, вы проиграли, дальнейшие ходы невозможны. Ваш счёт: {users_information[user_id]['score']}"
                    buttons.append({
                        "title": "Начать заново",
                    })
        else:
            text = "Неверная команда! Используюте кнопки влево/вправо/вниз/вверх"
    matrix = users_information[user_id]["matrix"][:][:]
    text += '\n' + "~" * 11 + '\n'
    for row in matrix:
        for number in row:
            if len(str(number)) == 1:
                text += '|  ' + str(number) + '  |'
            if len(str(number)) == 2:
                text += '| ' + str(number) + '  |'
            if len(str(number)) == 3:
                text += '|' + str(number) + '|'
        text += '\n'
    text += "~" * 11

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
    app.run(host='127.0.0.1', port=3000, ssl_context='adhoc')
