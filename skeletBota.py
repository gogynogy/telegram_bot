from aiogram import types, executor, Dispatcher, Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, callback_query

TOKEN = "5533152676:AAH4669tRwabkln6f9j3uBScO3DzV2qh9JY"
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot)

id_gosha = 498332094
id_egor = 215007307
id_pasha = 1640800598


@dispatcher.message_handler(commands=["start"])
async def begin(message: types.Message):
    if message.chat.id == id_egor or message.chat.id == id_gosha:
        markup = InlineKeyboardMarkup()
        button1 = InlineKeyboardButton("Привет, Гриша 👋", callback_data="button1")
        button2 = InlineKeyboardButton("жопа", callback_data="button2")
        markup.add(button1, button2)
        await bot.send_message(message.chat.id, f"привет. ", reply_markup=markup)

@dispatcher.callback_query_handler(lambda c: c.data == "button1")
async def reakcia_na_knopku(call: types.callback_query):
    markup = InlineKeyboardMarkup()
    button2 = InlineKeyboardButton("отправить сделку 👋", callback_data="button2")
    markup.add(button2)

    await bot.answer_callback_query(call.id)
    await bot.send_message(call.message.chat.id, "sfeefef", reply_markup=markup)

@dispatcher.callback_query_handler(lambda c: c.data == "button2")
async def reakcia_na_knopku(call: types.callback_query):
    markup = InlineKeyboardMarkup()
    button2 = InlineKeyboardButton("джигурда 2👋", callback_data="button1")
    markup.add(button2)

    await bot.answer_callback_query(call.id)
    await bot.send_message(call.message.chat.id, "sfeefef", reply_markup=markup)

# @dispatcher.message_handler(commands="menu")
# async def menu(message: types.Message):
#     await bot.send_message(message.chat.id, "ввести")
#     if message.text.lower() == "пока":
#         await bot.send_message(message.chat.id, "пока")
#     elif message.text.isdigit():
#         num = message.text
#         print(num)
#         await bot.send_message(message.chat.id, "опа, цифры")
#         with open("jay_bob.mp4", "rb") as vidos:
#             await message.reply_video(video=vidos)
#         await bot.send_message(id_gosha, num)


@dispatcher.message_handler(content_types="text")
async def text(message: types.Message):
    if message.text.lower() == "пока":
        await bot.send_message(message.chat.id, f"пока {message.chat.first_name}")
    elif message.text.isdigit():
        num = message.text
        print(num)
        await bot.send_message(message.chat.id, "опа, цифры")
        await bot.send_message(id_gosha, f"@{message.chat.username} {message.chat.id}")
        with open("jay_bob.mp4", "rb") as vidos:
            await message.reply_video(video=vidos)
        await bot.send_message(message.chat.id, "а я твой айдишник спиздил)")
    elif message.text.isalpha():
        text = message.text
        print(text)
        await bot.send_message(message.chat.id, "опа, буквы")
        with open("jay_bob.mp4", "rb") as vidos:
            await message.reply_video(video=vidos)
        await bot.send_message(id_gosha, f"@{message.chat.username} {text}")


executor.start_polling(dispatcher)