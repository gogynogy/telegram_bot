from aiogram import types, executor, Dispatcher, Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

TOKEN = "5576258137:AAEyUYoDd1MrY8wAfQ108cY9xoE2M3sk-b8"
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot)

with open("kuhnia.txt") as data:
    txt = data.readlines()

@dispatcher.message_handler(commands="start")
async def begin(message: types.Message):
    markup = InlineKeyboardMarkup
    button1 = InlineKeyboardButton("sesfsef", callback_data="button1")
    markup.add(button1)
    await bot.send_message(message.chat.id, 'hi hi', reply_markup=markup)
@dispatcher.message_handler(content_types="text")
async def text(message: types.Message):
    if message.text.lower() == "пока":
        await bot.send_message(message.chat.id, "пока")
    elif message.text.isdigit():
        num = message.text
        print(num)
        await bot.send_message(message.chat.id, "опа, цифры")




executor.start_polling(dispatcher)