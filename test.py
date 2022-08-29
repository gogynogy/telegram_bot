from aiogram import types, executor, Dispatcher, Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
import sqlite3, logging, time


with sqlite3.connect("arugamObmen.db") as arugamDB:
    sql = arugamDB.cursor()
    table = """CREATE TABLE IF NOT EXISTS obmen (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dateRegistration TEXT,
    dateStartWork TEXT,
    customerTelegram TEXT,
    customerPhone TEXT,
    customer TEXT,
    exchangeGroup TEXT,
    adminTelegram TEXT,
    adminEmpty TEXT,
    exchengeStart TEXT,
    waletStart TEXT,
    summStart TEXT,
    exchangeFinish TEXT,
    course TEXT,
    summFinish TEXT,
    moneyFrom TEXT,
    costOfUSDT TEXT,
    summUSDT TEXT,
    plusUSDT TEXT,
    memberTelegram TEXT,
    memberEmpty TEXT,
    agentTelegram TEXT,
    agentEmpty TEXT,
    agentCommisionUSDT TEXT,
    memberCommisionUSDT TEXT,
    dateOfTakeCash TEXT,
    paymentMethod TEXT,
    agent TEXT,
    statusInWork TEXT NOT NULL DEFAULT no,
    statusDone TEXT NOT NULL DEFAULT no,
    statusMoney TEXT NOT NULL DEFAULT no
    )"""
    sql.executescript(table)


logging.basicConfig(level=logging.INFO)
TOKEN = "5533152676:AAH4669tRwabkln6f9j3uBScO3DzV2qh9JY"
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot)
cb = CallbackData("id", "action")


id_gosha = 498332094
id_egor = 215007307
id_pasha = 1640800598
id_vania = 79994399


def location(target):#  направляет по разным локациям
    if target.lower() == "arugam":
        return id_gosha
    elif target.lower() == "trinko":
        return id_gosha


def createSQL(text):#  создает новую строку в таблице, возвращает id записи
    values = (time.asctime(), text[0], text[1], text[3], text[2], text[5], text[8], text[7], text[9], "+")
    sql.execute(f"INSERT INTO obmen (dateRegistration, customerTelegram, exchangeGroup, "
                f"exchengeStart, summStart, course, summFinish, "
                f"exchangeFinish, paymentMethod, statusInWork)"
                f" VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", values)
    arugamDB.commit()
    return sql.lastrowid

async def SendMessege(target, text, message, exchangeNum):
    await bot.send_message(target, f"Зарегистрирована сделка № {exchangeNum}\nКлиент: {text[0]}\n"
                                   f"Расшифровка сделки: {text[2]} {text[3]} @ {text[5]} = {text[7]} {text[8]}\n"
                                   f"Плановый профит сделки: ХYI USDT"
                                   f"Агент: <УКАЗАТЬ>  # (гиперссылка, нажимая выходишь на диалог с ботом по указанию агента, можно с преднастроенными кнопками для каждого агента)"
                                   f"Агент: НИК (плановая комиссия ХХХХ USDT)")  # , reply_markup=markup)
    # button = types.InlineKeyboardButton(text="Лайкнуть", callback_data=cb.new(id=exchangeNum))


async def SendMessegeAnswer(target, message, exchangeNum, text):
    await bot.send_message(message.chat.id, f" Инфа отправлена, номер сделки: {exchangeNum}\nCделка отправлена: {target}"
                                            f"Отправленный текст: {text}")





@dispatcher.message_handler(commands=["start"])
async def begin(message: types.Message):
    if message.chat.id == id_egor or message.chat.id == id_gosha:
        await bot.send_message(message.chat.id, f"привет. трудяги")
    else:
        await bot.send_message(message.chat.id, f"текст про то, что умеет бот")


@dispatcher.message_handler(content_types="text")
async def text(message: types.Message):
    text = message.text.split(" ")  # @Bombambaley arugam 20000 rur @ 5.6 = 112000 lkr binance
    print(text)
    if message.chat.id == id_egor or message.chat.id == id_gosha:
        if message.chat.id == id_egor or message.chat.id == id_gosha:# try:
            if text[2].isdigit() and text[7].isdigit():
                target = location(text[1])
                exchangeNum = createSQL(text)
                await SendMessege(target, text, message, exchangeNum)
                await SendMessegeAnswer(target, message, exchangeNum, text)
            else:
                await bot.send_message(message.chat.id, f"не получилось: {text}")
        else:
            await bot.send_message(message.chat.id, f"не получилось: {text}")
    else:
        if text[0].startswith("@"):
            try:
                await bot.send_message(id_egor, f"перевод по обмену для {text[0]}\n"
                                                f"отправлено на бинанс: {text[1]} {text[2]}")
                sql.execute(f"INSERT INTO")
                await bot.send_message(message.chat.id, "информация о платеже принята")
            except:
                await bot.send_message(message.chat.id, "неверный формат ввода: @example 420 usdt")
        elif text[0].lower().startswith("заявка"):
            await bot.send_message(id_egor, message.text)
            await bot.send_message(message.chat.id, "заявка на обмен отправлена")
        elif text[0].lower() == "пока":
            await bot.send_message(message.chat.id, f"пока {message.chat.first_name}")
        elif text[0].isdigit():
            num = message.text
            print(num)
            await bot.send_message(message.chat.id, "опа, цифры")
            # await bot.send_message(id_gosha, f"@{message.chat.username} {message.chat.id}") #присылает мне в личку id
            # await bot.send_message(message.chat.id, "а я твой айдишник спиздил)")
            with open("jay_bob.mp4", "rb") as vidos:
                await message.reply_video(video=vidos)
        elif text[0].isalpha():
            text = message.text
            print(text)
            await bot.send_message(message.chat.id, "опа, буквы")
            with open("jay_bob.mp4", "rb") as vidos:
                await message.reply_video(video=vidos)
            await bot.send_message(id_gosha, f"@{message.chat.username} {text}")

# @dispatcher.callback_query_handler(cb.filter(item_name="startExchange"))
# async def callbacks_num_change_fab(call: types.CallbackQuery, callback_data: dict):
#     print("dsgvs")


executor.start_polling(dispatcher, skip_updates=True)