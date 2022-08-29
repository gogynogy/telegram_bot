from aiogram import types, executor, Dispatcher, Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, callback_query

TOKEN = "5576258137:AAEyUYoDd1MrY8wAfQ108cY9xoE2M3sk-b8"
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot)

id_pasha = 1640800598
id_gosha = 498332094

# with open("kuhnia.txt") as data:
#     txt = data.readlines()

@dispatcher.message_handler(commands=["start"])
async def begin(message: types.Message):
    markup = InlineKeyboardMarkup()
    button1 = InlineKeyboardButton("sesfsef", callback_data="button1")
    markup.add(button1)

    await bot.send_message(message.chat.id, "hi hi", reply_markup=markup)
#
# @dispatcher.callback_query_handler(lambda c: c.data == "button1")
# async def button_reaction(call: types.callback_query):
#     await  bot.answer_callback_query(call.id)
#     await bot.send_message(call.massege.chat.id, "srgsrg")

@dispatcher.message_handler(content_types="text")
async def text(message: types.Message):
    if message.text.lower() == "пока":
        await bot.send_message(message.chat.id, f"пока {message.chat.id}")
    elif message.text.isdigit():
        num = message.text
        print(num)
        await bot.send_message(message.chat.id, "опа, цифры")
    elif message.text.isalpha():
        text = message.text
        print(text)
        await bot.send_message(message.chat.id, "опа, буквы")
        with open("jay_bob.mp4", "rb") as vidos:
            await message.reply_video(video=vidos)
        await bot.send_message(id_gosha, f"{message.chat.id}text")



executor.start_polling(dispatcher)