import random

import telebot
from telebot import types
import time
import schedule
from threading import Thread

user_name = ""
time_set = "09:00"
emoji_love = ["😘", "❤", "💕", "💋", "✨", "💖", "🥰"]
last_command = ""

bot = telebot.TeleBot("5017889526:AAHU6ExmufVnabKqA5UBZPlIKmvr2IPtJjw")


def send_hello():
    global id
    generation_emoji = ""
    for x in range(10):
        generation_emoji = f"{generation_emoji}{emoji_love[random.randint(0, 6)]}"

    markup = types.InlineKeyboardMarkup()
    buttonOne = types.InlineKeyboardButton("хорошо", callback_data="good")
    buttonTwo = types.InlineKeyboardButton("плохо", callback_data="bad")
    markup.row(buttonOne, buttonTwo)

    bot.send_message(id, f'привет дорогуша!{generation_emoji}\nКак у тебя дела?', reply_markup=markup)


@bot.message_handler(commands=['start'])
def start(message):
    global id
    global emoji_love
    generation_emoji = ""
    for x in range(10):
        generation_emoji = f"{generation_emoji}{emoji_love[random.randint(0, 6)]}"
    id = message.chat.id
    pid = random.randint(1, 6)
    photoid = f"photo{pid}.jpg" if pid != 2 and pid != 3 else f"photo{pid}.gif"
    bot.send_photo(message.chat.id, open(f'{photoid}', 'rb'))
    bot.send_message(message.chat.id, f"Привет, привет! Я рада знакомству!{generation_emoji}\nМеня зовут Люси.\nА к тебе как обращаться?")
    global last_command
    last_command = "say_name"


@bot.callback_query_handler(func=lambda call: call.data == "good")
def callback(call):
    global emoji_love
    generation_emoji = ""
    for x in range(10):
        generation_emoji = f"{generation_emoji}{emoji_love[random.randint(0, 6)]}"
    bot.send_message(call.message.chat.id, f"Я очень рада за вас!{generation_emoji}")


@bot.message_handler(content_types=["text"])
def set_city(message):
    global time_set
    global last_command
    global job
    global user_name
    if message.text == "привет":
        time_set = [str(time.localtime().tm_hour), str(time.localtime().tm_min)]
        if len(time_set[0]) == 2 or len(time_set[0]) == 1:
            if len(time_set[1]) == 2 and len(time_set[0]) != 1:
                send_hello()
                schedule.cancel_job(job)
                job = schedule.every().day.at(f"{message.text}").do(send_hello)
            elif len(time_set[1]) == 2 and len(time_set[0]) == 1:
                send_hello()
                schedule.cancel_job(job)
                job = schedule.every().day.at(f"0{message.text}").do(send_hello)
    elif last_command == "say_name":
        user_name = message.text
        last_command = ""
        global emoji_love
        generation_emoji = ""
        for x in range(10):
            generation_emoji = f"{generation_emoji}{emoji_love[random.randint(0, 6)]}"
        bot.send_message(message.chat.id, f"Рада знакомству {user_name}! {generation_emoji}")


def schedule_checker():
    while True:
        schedule.run_pending()


job = schedule.every().day.at(time_set).do(send_hello)
Thread(target=schedule_checker).start()


def schedule_checker1():
    while True:
        time.sleep(120)
        print("time processing")


job1 = schedule.every().day.at(time_set).do(send_hello)
Thread(target=schedule_checker1).start()

bot.polling(none_stop=True, interval=0)