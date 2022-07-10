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
    return f'<h1>{"https" + request.base_url[4:]}webhook</h1>'


@app.route('/marusya', methods=['POST', 'GET'])
def marusya():
    return "Marusya"


users_information = {}

cards = {"Туз": 11, "Валет": 2, "Дама": 3, "Король": 4, "Шестерка": 6, "Семерка": 7, "Восьмерка": 8, "Девятка": 9,
         "Десятка": 10}
card_suits = ["Черви", "Пики", "Бубны", "Крести"]


@app.route('/ten/webhook', methods=['POST'])
def webhook():
    user_id = request.json["session"]["user_id"]
    message = request.json['request']['original_utterance'].lower().split()
    if message[0] == 'старт':
        users_information[user_id] = {"game_status": 0, "computer": 0, "player": 0, "wins": 0, "loses": 0}
        text = f"Запущена игра 'Двадцать одно'!\n"
    else:
        text = ""

    try:
        users_information[user_id]["game_status"]
    except KeyError as user_not_in_db_error:
        users_information[user_id] = {"game_status": 0, "computer": 0, "player": 0}

    if users_information[user_id]['computer'] == 0:
        new_card = choice(list(cards.keys()))
        users_information[user_id]['computer'] += cards[new_card]
        text += f"Я вытянула карту {new_card + ' ' + choice(card_suits)}\n"
        new_card = choice(list(cards.keys()))
        users_information[user_id]['player'] += cards[new_card]
        text += f"Вы вытянули карту {new_card + ' ' + choice(card_suits)}\n"
        new_card = choice(list(cards.keys()))
        users_information[user_id]['player'] += cards[new_card]
        text += f"Вы вытянули карту {new_card + ' ' + choice(card_suits)}\n"
        users_information[user_id]['game_status'] = 1
    else:
        if message[0] == "ещё" or message[0] == "еще":
            new_card = choice(list(cards.keys()))
            users_information[user_id]['player'] += cards[new_card]
            text += f"Вы вытянули карту {new_card + ' ' + choice(card_suits)}\n"
            if users_information[user_id]['player'] >= 22:
                text += "У вас перебор! Вы проиграли.\n"
                users_information[user_id]['loses'] += 1
                users_information[user_id]['game_status'] = 0
        elif message[0] == "нет":
            users_information[user_id]['game_status'] = 0
            while users_information[user_id]['computer'] <= 16:
                new_card = choice(list(cards.keys()))
                users_information[user_id]['computer'] += cards[new_card]
                text += f"Я вытянула карту {new_card + ' ' + choice(card_suits)}\n"
            if users_information[user_id]['computer'] >= 22:
                text += "У меня перебор. Победа в раунде ваша.\n"
                users_information[user_id]['wins'] += 1
            else:
                if users_information[user_id]['computer'] > users_information[user_id]['player']:
                    text += "Я ближе к 21 очку. К сожалению, вы проиграли.\n"
                    users_information[user_id]['loses'] += 1
                elif users_information[user_id]['computer'] == users_information[user_id]['player']:
                    text += "Ничья.\n"
                else:
                    text += "Вы ближе к 21 очку. Победа в раунде ваша.\n"
                    users_information[user_id]['wins'] += 1
        else:
            text = "Неправильная команда!\n" \
                   "Чтобы взять ещё карту - введите 'Ещё'" \
                   "Чтобы прекратить - введите 'Нет'\n"
    text += "Счёт в раунде:\n" \
            f"Я: {users_information[user_id]['computer']}\nВы: {users_information[user_id]['player']}\n"
    text += "Счёт всех игр:\n" \
            f"Ваших побед: {users_information[user_id]['wins']}\nВаших поражений: {users_information[user_id]['loses']}\n"
    if users_information[user_id]['game_status'] == 1:
        text += "Ещё?"
    else:
        text += "Следующая партия...\n"

        users_information[user_id]['computer'] = 0
        users_information[user_id]['player'] = 0

        new_card = choice(list(cards.keys()))
        users_information[user_id]['computer'] += cards[new_card]
        text += f"Я вытянула карту {new_card + ' ' + choice(card_suits)}\n"
        new_card = choice(list(cards.keys()))
        users_information[user_id]['player'] += cards[new_card]
        text += f"Вы вытянули карту {new_card + ' ' + choice(card_suits)}\n"
        new_card = choice(list(cards.keys()))
        users_information[user_id]['player'] += cards[new_card]
        text += f"Вы вытянули карту {new_card + ' ' + choice(card_suits)}\n"

        text += "Счёт в раунде:\n" \
                f"Я: {users_information[user_id]['computer']}\nВы: {users_information[user_id]['player']}\n"
        users_information[user_id]['game_status'] = 1

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

    btn_more = {
        "title": "Ещё",
    }
    btn_enough = {
        "title": "Нет",
    }
    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False,
            "text": text,
            "tts": tts,
            "card": {},
            "buttons": [btn_more, btn_enough]
        }
    }

    return json.dumps(response, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    app.run(port=3000)
