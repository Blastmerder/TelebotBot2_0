import telebot
from telebot import types
import time
from WeatherForecast import WeatherForecast
import schedule
from threading import Thread

time_set = "07:00"

last_command = ""

bot = telebot.TeleBot("5017889526:AAHU6ExmufVnabKqA5UBZPlIKmvr2IPtJjw")
weather_forecast = WeatherForecast()

bot.set_my_commands([
    types.BotCommand("set_city", "Вам дадут инструкции"),
    types.BotCommand("set_lang", "Вам дадут инструкции"),
    types.BotCommand("set_units", "Вам дадут инструкции"),
    types.BotCommand("set_time_mesage", "Вам дадут инструкции"),
    types.BotCommand("schedule", "Вам дадут инструкции")
])


@bot.message_handler(commands=["schedule"])
def schedulee(message):
    global id
    id = message.chat.id
    bot.send_message(id, "введите время в которое вы\nхотите получить сообщение")
    global last_command
    last_command = "schedule"


def send_hello():
    global id
    bot.send_message(id, f'Сейчас в городе {weather_forecast.get_data().json()["name"]} {weather_forecast.get_data().json()["weather"][0]["description"]}.')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Введите свой город")
    global last_command
    last_command = "start"


@bot.message_handler(commands=['set_city'])
def start(message):
    bot.send_message(message.chat.id, "Введите свой город")
    global last_command
    last_command = "start"


@bot.message_handler(commands=['set_units'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    buttonOne = types.InlineKeyboardButton("метричная система", callback_data="metric")
    buttonTwo = types.InlineKeyboardButton("имперская система", callback_data="imperic")
    markup.row(buttonOne, buttonTwo)

    bot.send_message(message.chat.id, "Выбери свою систему счёта", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "metric")
def callback(call):
    weather_forecast.set_units("metric")
    bot.send_message(call.message.chat.id, "успешно установлена метрическая система.")


@bot.callback_query_handler(func=lambda call: call.data == "imperic")
def callback(call):
    weather_forecast.set_units("imperic")
    bot.send_message(call.message.chat.id, "успешно установлена импееская система.")


@bot.message_handler(commands=['set_lang'])
def set_lang(message):
    bot.send_message(message.chat.id, "Введите свой язык")
    global last_command
    last_command = "set_lang"


@bot.message_handler(commands=['weather'])
def get_weather(message):
    bot.send_message(message.chat.id, f'Сейчас в городе {weather_forecast.get_data().json()["name"]} {weather_forecast.get_data().json()["weather"][0]["description"]}.')


@bot.message_handler(content_types=["text"])
def set_city(message):
    global time_set
    global last_command
    global job
    if last_command == "start":
        if weather_forecast.set_city(message.text):
            bot.send_message(message.chat.id, f"успешно установлен город {message.text}")
            last_command = ""
        else:
            bot.send_message(message.chat.id, "Введите свой город ещё раз")
    elif last_command == "set_lang":
        if weather_forecast.set_lang(message.text):
            bot.send_message(message.chat.id, f"успешно установлен язык {message.text}")
            last_command = ""
        else:
            bot.send_message(message.chat.id, "Введите свой язык ещё раз")
    elif last_command == "set_units":
        if weather_forecast.set_lang(message.text):
            bot.send_message(message.chat.id, f"успешно установлена единица измерения {message.text}")
            last_command = ""
        else:
            bot.send_message(message.chat.id, "Введите свои единицы измерения ещё раз")
    elif last_command == "schedule":
        time_set = message.text.split(":")
        if len(time_set[0]) == 2 or len(time_set[0]) == 1:
            if len(time_set[1]) == 2 and len(time_set[0]) != 1:
                bot.send_message(message.chat.id, f"успешно установлено время {message.text}")
                last_command = ""
                schedule.cancel_job(job)
                job = schedule.every().day.at(f"{message.text}").do(send_hello)
            elif len(time_set[1]) == 2 and len(time_set[0]) == 1:
                bot.send_message(message.chat.id, f"успешно установлено время {message.text}")
                last_command = ""
                schedule.cancel_job(job)
                job = schedule.every().day.at(f"0{message.text}").do(send_hello)
        else:
            bot.send_message(message.chat.id, "Введите свои единицы измерения ещё раз")


def schedule_checker():
    while True:
        schedule.run_pending()


job = schedule.every().day.at(time_set).do(send_hello)
Thread(target=schedule_checker).start()

bot.polling(none_stop=True, interval=0)