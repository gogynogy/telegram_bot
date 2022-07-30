import telebot
from pyowm.owm import OWM

from pyowm.utils.config import get_default_config
config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = OWM('f46dbe357f9f0a87de2b49e873bb2e75', config_dict)

bot = telebot.TeleBot("5094612612:AAGCh1opkdk3EINXoe_fxUZDluLh-gFz650")

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Привет, в каком городе интересует погода?")

@bot.message_handler(commands=['help'])
def send_welcome(message):
	bot.reply_to(message, "помоги себе сам, псина горбатая")

@bot.message_handler(commands=['boobs'])
def send_massege(messege):
    gif = open('221928.gif', 'rb')
    bot.send_document(messege.chat.id, gif)

@bot.message_handler(content_types=['text'])
def send_echo(message):
    try:
        observation = owm.weather_manager().weather_at_place(message.text)
        w = observation.weather
        temp = w.temperature('celsius')['feels_like']
        answer = f"в городе {message.text} сейчас {w.detailed_status} и ощущается это говно на {str(int(temp))} градусов."
        bot.send_message(message.chat.id, answer)
    except:
        answer = f"{message.text}... i dont ebu, где такие ебеня находятся"
        bot.send_message(message.chat.id, answer)
bot.polling(none_stop = True)