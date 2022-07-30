import telebot
from telebot import types

bot = telebot.TeleBot("5533152676:AAH4669tRwabkln6f9j3uBScO3DzV2qh9JY")
# bot2 = telebot.TeleBot("5094612612:AAGCh1opkdk3EINXoe_fxUZDluLh-gFz650")

@bot.message_handler(commands=['start'])
def start(messege):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('menu')
    markup.add(item1)

    bot.send_message(messege.chat.id, f"Здраствуйте, {messege.from_user.username}!\n\n"
                                      f"ВАМ НУЖНЫ ШРИ-ЛАНКИЙСКИЕ РУПИИ ИЛИ USD?\n\n"
                                      f"Оставьте заявку в данном боте и получите предложения сразу от нескольких "
                                      f"обменников, работающих в Вашем городе!\nПриглашаем к сотрудничеству новые "
                                      f"обменники! ☺️\nТак же мы готовы предоставить "
                                      f"информацию для тех, кто хочет стать"
                                      f" обменником, но пока не знает как. Обучим!\nТвоя реферальная ссылка: ссылка\n"
                                      f"Приглашай новых пользователей и зарабатывай с нами!!!\nПодробнсти реферальной "
                                      f"программы смотри в разделе 'help'.", reply_markup=markup)

@bot.message_handler(content_types=["text"])
def bot_messege(messege):
    if messege.text == 'menu':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('dick')
        item2 = types.KeyboardButton('boobs')
        markup.add(item1, item2)
        bot.send_message(messege.chat.id, 'menu', reply_markup=markup)
    elif messege.text == 'boobs':
        gif = open('221928.gif', 'rb')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('menu')
        markup.add(item1)
        bot.send_document(messege.chat.id, gif, reply_markup=markup)
        gif.close()
    elif messege.text == 'dick':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('menu')
        markup.add(item1)
        bot.send_message(messege.chat.id, "i dont ebu, чем помочь тебе.", reply_markup=markup)



bot.polling(none_stop = True)