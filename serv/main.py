from __future__ import unicode_literals
from flask import Flask, request
from flask_cors import CORS
from random import choice

import json
import logic
import snake

app = Flask(__name__)
app.debug = True
CORS(app)


@app.route('/')
def index():
    s = ""
    s += f'<h1>{"https" + request.base_url[4:]}ten/webhook</h1>\n'
    s += f'<h1>{"https" + request.base_url[4:]}twenty/webhook</h1>\n'
    s += f'<h1>{"https" + request.base_url[4:]}forty/webhook</h1>\n'
    s += f'<h1>{"https" + request.base_url[4:]}fifty/webhook</h1>\n'
    return s


users_information = {}
# Данные для игры 1
cards = {"Туз": 11, "Валет": 2, "Дама": 3, "Король": 4, "Шестерка": 6, "Семерка": 7, "Восьмерка": 8, "Девятка": 9,
         "Десятка": 10}
card_suits = ["Черви", "Пики", "Бубны", "Крести"]

# Данные для игры 2
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
    "Лиду": 0,
    "раздаточную коробку": 0,
    "провода": 0,
    "мармелад": 1,
    "сырники": 1,
    "маскарпоне": 1,
}


@app.route('/ten/webhook', methods=['POST'])
def ten_webhook():
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
    text += "Очки в раунде:\n" \
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

        text += "Очки в раунде:\n" \
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


@app.route('/twenty/webhook', methods=['POST'])
def twenty_webhook():
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


@app.route('/forty/webhook', methods=['POST'])
def forty_webhook():
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
               f"Управляйте змейкой командами влево/вправо/вниз/вверх, удачи!\n"
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
                    users_information[user_id]["matrix"], users_information[user_id]["body"], \
                    users_information[user_id]["score"], error = snake.move_left(users_information[user_id]["matrix"],
                                                                                 users_information[user_id]["body"],
                                                                                 users_information[user_id]["score"])
                if message[0] == "вправо":
                    users_information[user_id]["matrix"], users_information[user_id]["body"], \
                    users_information[user_id]["score"], error = snake.move_right(users_information[user_id]["matrix"],
                                                                                  users_information[user_id]["body"],
                                                                                  users_information[user_id]["score"])
                if message[0] == "вниз":
                    users_information[user_id]["matrix"], users_information[user_id]["body"], \
                    users_information[user_id]["score"], error = snake.move_down(users_information[user_id]["matrix"],
                                                                                 users_information[user_id]["body"],
                                                                                 users_information[user_id]["score"])
                if message[0] == "вверх":
                    users_information[user_id]["matrix"], users_information[user_id]["body"], \
                    users_information[user_id]["score"], error = snake.move_up(users_information[user_id]["matrix"],
                                                                               users_information[user_id]["body"],
                                                                               users_information[user_id]["score"])
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


@app.route('/fifty/webhook', methods=['POST'])
def fifty_webhook():
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
               f"Управляйте игрой командами влево/вправо/вниз/вверх, удачи!\n"
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
    text += '\n' + "~" * 14 + '\n'
    for row in matrix:
        for number in row:
            if len(str(number)) == 1:
                text += '|_' + str(number) + '_|'
            if len(str(number)) == 2:
                text += '|.' + str(number) + '.|'
            if len(str(number)) == 3:
                text += '|' + str(number) + '|'
        text += '\n'
    text += "~" * 14
    text = text.replace("||", "|")

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
    app.run(port=5046)
