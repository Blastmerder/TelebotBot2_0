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

bot = telebot.TeleBot("5102757220:AAGUZy8_esTuD0HrnE666Pd_p2vSTtC5Kk0")


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
    bot.send_message(message.chat.id, f"Привет, привет! {generation_emoji}\nМеня зовут Люси.\nА к тебе как обращаться?")
    global last_command
    last_command = "say_name"


@bot.message_handler(commands=['привет'])
def start(message):
    send_hello()


@bot.callback_query_handler(func=lambda call: call.data == "good")
def callback(call):
    global emoji_love
    generation_emoji = ""
    for x in range(10):
        generation_emoji = f"{generation_emoji}{emoji_love[random.randint(0, 6)]}"

    markup = types.InlineKeyboardMarkup()
    buttonOne = types.InlineKeyboardButton("Расскажи анекдот", callback_data="SayAnegdot")
    buttonTwo = types.InlineKeyboardButton("включи музыку", callback_data="song")
    buttonTree = types.InlineKeyboardButton("ничего ненадо", callback_data="Don't")
    markup.row(buttonOne, buttonTwo, buttonTree)

    bot.send_message(call.message.chat.id, f"Я очень рада за вас!{generation_emoji}\nХотите я расскажу анекдот?\nИли музыку включу!", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "SayAnegdot")
def callback(call):
    anegdot = open("anigdot.txt", "r", encoding="UTF-8")
    a = str(anegdot.read()).split("\n")
    ra = (a[random.randint(0, 9)]).replace('/', f'\n')
    bot.send_message(call.message.chat.id, f"{ra}")


@bot.callback_query_handler(func=lambda call: call.data == "song")
def callback(call):
    anegdot = open("Испанская_гитара.txt", "r", encoding="UTF-8")
    a = str(anegdot.read()).split("\n")
    print(a)
    audi = f"Испанская гитара\\{a[random.randint(0, 16)]}"
    audio = open(rf'{audi}', 'rb')
    bot.send_audio(call.message.chat.id, audio)
    audio.close()


@bot.callback_query_handler(func=lambda call: call.data == "bad")
def callback(call):
    markup = types.InlineKeyboardMarkup()
    buttonOne = types.InlineKeyboardButton("да", callback_data="angry")
    buttonTwo = types.InlineKeyboardButton("нет", callback_data="notLeg")
    markup.row(buttonOne, buttonTwo)

    bot.send_message(call.message.chat.id, f"Вас обидели?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "notLag")
def callback(call):
    bot.send_message(call.message.chat.id, f"Скем не бывает...")


@bot.callback_query_handler(func=lambda call: call.data == "angry")
def callback(call):
    markup = types.InlineKeyboardMarkup()
    buttonOne = types.InlineKeyboardButton("да", callback_data="angry2")
    buttonTwo = types.InlineKeyboardButton("нет", callback_data="not")
    markup.row(buttonOne, buttonTwo)

    bot.send_message(call.message.chat.id, f"Разрешите я прокляну вашего обитчика? 😈😈😈😈", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "not")
def callback(call):
    bot.send_message(call.message.chat.id, "Хорошо, пусть останется безнаказанным.")


@bot.callback_query_handler(func=lambda call: call.data == "angry2")
def callback(call):
    bot.send_message(call.message.chat.id, "Проклинаю вашего обидчика, подождите...")
    time.sleep(5)
    bot.send_message(call.message.chat.id, "Я навела порчу на обидчика.\nДа свершится правосудие!!!")


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