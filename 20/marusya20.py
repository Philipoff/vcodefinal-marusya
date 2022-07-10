from __future__ import unicode_literals
import json
from flask import Flask, request
from flask_cors import CORS
from random import choice

app = Flask(__name__)
app.debug = True
CORS(app)


# client = MongoClient(
#     "mongodb://vcodebackend:vcodebackend@194.67.111.141:27017/vcodebackend?authSource=vcodebackend&readPreference"
#     "=primary&directConnection=true&ssl=false")
# quiz_collecion = client["vcodebackend"]["quiz"]


@app.route('/')
def index():
    return f'<h1>{"https" + request.base_url[4:]}twenty/webhook</h1>'


users_information = {}

food_or_not = {
    "белый гриб": 1,
    "дверь": 0,
    "черноплодную рябину": 1,
    "капусту": 1,
    "робусту": 1,
    "морского черта": 1,
    "костянику": 1,
    "мухомор": 0,
    "карамболь": 1,
    "казан": 0,
    "гуаву": 1,
    "бурмиллу": 0,
    "волчье лыко": 0,
    "шелковицу": 1,
    "яблоко": 1,
    "стул": 0,
    "ежа": 0,
    "раздаточную коробку": 0,
    "провода": 0,
    "мармелад": 1,
    "сырники": 1,
    "маскарпоне": 1,
}


@app.route('/twenty/webhook', methods=['POST'])
def webhook():
    text = ''

    user_id = request.json["session"]["user_id"]
    message = request.json['request']['original_utterance'].lower().split()
    try:
        users_information[user_id]["score"]
    except KeyError as user_not_in_db_error:
        users_information[user_id] = {"score": 0, "last_item": ""}
    if message[0] == 'старт':
        text = f"Запущена игра 'Съедобное — несъедобное'!\n"
        users_information[user_id] = {"score": 0, "last_item": ""}
    if users_information[user_id]['last_item']:
        if message[0] == 'съем' or message[0] == 'выброшу':
            if (message[0] == 'съем' and food_or_not[users_information[user_id]['last_item']]) or (
                    message[0] == 'выброшу' and not food_or_not[users_information[user_id]['last_item']]):
                text = "Правильный ответ!\n"
                users_information[user_id]['score'] += 1
            else:
                text = "Неправильно! К сожалению, счёт обнуляется.\n"
                users_information[user_id]['score'] = 0
        else:
            text = "Неизвестная команда..." \
                   "Отвечайте с помощью съем/выброшу\n"
    text += f"Счёт: {users_information[user_id]['score']}\n"
    eat_or_not_item = choice(list(food_or_not.keys()))
    text += f"Съешь ли ты {eat_or_not_item}?"
    users_information[user_id]['last_item'] = eat_or_not_item

    tts = ""
    brackets_count = 0
    for i in text:
        if i == "<":
            brackets_count += 1
        elif i == ">":
            brackets_count -= 1
        elif brackets_count == 0:
            tts += i
    tts, text = text, tts

    btn_yes = {
        "title": "Съем",
    }
    btn_no = {
        "title": "Выброшу",
    }
    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False,
            "text": text,
            "tts": tts,
            "buttons": [btn_yes, btn_no]
        }
    }

    return json.dumps(response, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    app.run(port=3000)
