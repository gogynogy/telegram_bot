from aiogram import types, executor, Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
import sqlite3
import logging
import time

with sqlite3.connect("../arugamObmen.db") as arugamDB:
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
    agent TEXT NOT NULL DEFAULT egor,
    statusInWork TEXT NOT NULL DEFAULT no,
    statusDone TEXT NOT NULL DEFAULT no,
    statusMoney TEXT NOT NULL DEFAULT no
    )"""
    sql.executescript(table)

logging.basicConfig(level=logging.INFO)
TOKEN = "5533152676:AAH4669tRwabkln6f9j3uBScO3DzV2qh9JY"
storage = MemoryStorage()
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot=bot,
                        storage=storage)
cb = CallbackData('button1', 'msg_id')

class FSMReg(StatesGroup):
    CountNumber = State()
    Course = State()


id_gosha = 498332094
id_egor = 215007307
id_pasha = 1640800598
id_vania = 79994399


def location(target):  #направляет по разным локациям
    if target.lower() == "arugam":
        return id_gosha
    elif target.lower() == "trinko":
        return id_gosha


def vozvrat_id(id_zapisi):  #создает кнопку с id записи
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(f'открыть сделку {id_zapisi}', callback_data=cb.new(msg_id=id_zapisi))]
        ]
    )


@dispatcher.callback_query_handler(cb.filter())  #возвращает номер открытой сделки и открывает строчку в таблице
async def button_hendler(query: types.CallbackQuery, callback_data: dict):
    message_id = callback_data.get('msg_id')
    string = openSQL(message_id)
    await query.message.answer(text=string)



def createSql(text):  #создает новую строку в таблице, возвращает id записи
    values = (time.asctime(), text[0], text[1], text[3], text[2], text[5], text[8], text[7], text[9], text[10], "+")
    sql.execute(f"INSERT INTO obmen (dateRegistration, customerTelegram, exchangeGroup, "
                f"exchengeStart, summStart, course, summFinish, "
                f"exchangeFinish, paymentMethod, agent, statusInWork)"
                f" VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", values)
    arugamDB.commit()
    return sql.lastrowid


def openSQL(strNum): # возврвщвет сделку по заданному id для админа
    try:
        with sqlite3.connect("../arugamObmen.db") as arugamDB:
            sql = arugamDB.cursor()
            sql.execute("""SELECT * FROM obmen WHERE id = ?""", [strNum])
            return sql.fetchone()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)


def openSQLAgent(strNum): # возврвщвет сделку по заданному id для агента
    try:
        with sqlite3.connect("../arugamObmen.db") as arugamDB:
            sql = arugamDB.cursor()
            sql.execute("""SELECT customerTelegram, summStart, course, summFinish FROM obmen WHERE id = ?""", [strNum])
            return sql.fetchone()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)


def addSQL(idTelega, parametr, count):  # обновляет заданный параметр в sql по одному
    try:
        with sqlite3.connect("../arugamObmen.db") as arugamDB:
            sql = arugamDB.cursor()
            sql.execute("""UPDATE obmen SET {} = {} WHERE id = {}""".format(parametr, count, idTelega))
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)


@dispatcher.callback_query_handler(lambda c: c.data == "openOrders")  #сообщает о не закрытых сделках
async def reakcia_na_knopku(call: types.callback_query):
    try:
        with sqlite3.connect("../arugamObmen.db") as arugamDB:
            sql = arugamDB.cursor()
            sql.select_query = """SELECT id, customerTelegram FROM obmen WHERE statusDone != ?"""
            sql.execute(sql.select_query, ("done",))
            records = sql.fetchall()
            await bot.send_message(call.message.chat.id, records)
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)


async def SendMessege(target, text, message, exchangeNum):
    await bot.send_message(target, f"Зарегистрирована сделка № {exchangeNum}\nКлиент: {text[0]}\n"
                                   f"Расшифровка сделки: {text[2]} {text[3]} @ {text[5]} = {text[7]} {text[8]}\n"
                                   f"Плановый профит сделки: ХYI USDT"
                                   f"Агент: <УКАЗАТЬ>  # (гиперссылка, нажимая выходишь на диалог с ботом по указанию агента, можно с преднастроенными кнопками для каждого агента)"
                                   f"Агент: НИК (плановая комиссия ХХХХ USDT)")


async def SendMessegeAnswer(target, message, exchangeNum, text):
    button = vozvrat_id(exchangeNum)
    await bot.send_message(target, f"Инфа отправлена, номер сделки: {exchangeNum}\n"
                                            f"Cделка отправлена: @{message.chat.username}\n"
                                            f"Отправленный текст: {text}", reply_markup=button)


def cancelOperation():  #кнопка закрывания текущего действия
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(f'отменить заполнение', callback_data="cancel")]
        ]
    )

@dispatcher.callback_query_handler(lambda c: c.data == "cancel", state="*")  #закрывает текущее действие
async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Заполнение прекращено")


@dispatcher.callback_query_handler(lambda c: c.data == 'continueReg', state=None)  #запрашивает номер заполняемой сделки
async def continueReg(call: types.callback_query):  #/continueReg
    await bot.send_message(call.message.chat.id, "сделку с каким номером открыть?", reply_markup=cancelOperation())
    await FSMReg.CountNumber.set()


@dispatcher.message_handler(state=FSMReg.CountNumber)  #запрашивает курс USDT
async def ShowNotFullReg(message: types.Message, state: FSMContext):
    global countNum
    countNum = message.text
    await state.update_data(countNumber=countNum)
    await message.answer(openSQL(countNum))
    await FSMReg.Course.set()
    await message.answer("Введите курс по которому закупался USDT", reply_markup=cancelOperation())


@dispatcher.message_handler(state=FSMReg.Course)  #сохраняет курс USDT запрашивает
async def CourseChoise(message: types.Message, state: FSMContext):
    course, perametr = message.text, "costOfUSDT"
    addSQL(countNum, perametr, course)
    await state.update_data(Course=course)
    await message.answer(course, reply_markup=cancelOperation())


@dispatcher.message_handler(commands=["start"])
async def begin(message: types.Message):
    if message.chat.id == id_egor:# or message.chat.id == id_gosha:
        markup = InlineKeyboardMarkup(row_width=1)
        button1 = InlineKeyboardButton("Not work", callback_data="NewSdelka")
        button2 = InlineKeyboardButton("Не завершенные сделки", callback_data="openOrders")
        button3 = InlineKeyboardButton("Продолжить заполнение сделки", callback_data="continueReg")
        markup.add(button1, button2, button3)
        await message.answer(f"Привет\nТрудяги)", reply_markup=markup)
    else:
        await message.answer(f"Если отправить просто цифру, откроет сделку с соответствующим id.\n"
                             f"Для закрытие сделки, отправь информацию в формате: '42 @example 420 usdt'")

@dispatcher.message_handler(content_types="text")
async def text(message: types.Message):
    text = message.text.split(" ")  # @Bombambaley arugam 20000 rur @ 5.6 = 112000 lkr binance artist
    if message.chat.id == id_egor or message.chat.id == id_gosha:
        try:
            if len(text) == 1 and text[0].isdigit():
                num = message.text
                await bot.send_message(message.chat.id, openSQL(num))
            elif text[2].isdigit() and text[7].isdigit():
                target = location(text[1])
                exchangeNum = createSql(text)
                await SendMessege(target, text, message, exchangeNum)
                await SendMessegeAnswer(target, message, exchangeNum, text)
            else:
                await bot.send_message(message.chat.id, f"не получилось: {text}")
        except Exception as error:
            print(error)
    else:
        if len(text) == 1 and text[0].isdigit():  # если пришла цифра, открывает сделку с таким номером
            try:
                num = message.text
                await bot.send_message(message.chat.id, openSQLAgent(num))
            except Exception as error:
                print(error)
        elif text[0].isdigit():  # 42 @example 420 usdt
            try:
                parametr = "summUSDT"
                addSQL(text[1], parametr, text[2])
                await bot.send_message(id_gosha, f"перевод по обмену для {text[0]}\n"
                                                f"отправлено на бинанс: {text[1]} {text[2]}")

                await bot.send_message(message.chat.id, "информация о платеже принята")
            except:
                await bot.send_message(message.chat.id, "неверный формат ввода: 42 @Primer 420 usdt")




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


# @dispatcher.callback_query_handler(lambda c: c.data == "NewSdelka")
# async def reakcia_na_knopku(call: types.callback_query):
#     text = ['@Клиент', 'локация', 'сумма в стартовой валюте', 'стартовая валюта', '@', 'курс', '=', 'сумма обмена',
#             'валюта обмена', 'способ платежа', 'контрагент']
#     markup = InlineKeyboardMarkup()
#     button1 = InlineKeyboardButton("Клиент", callback_data="createClient")
#     button10 = InlineKeyboardButton("Сбросить все и вернуться в начало", callback_data="NewSdelka")
#     markup.add(button1, button10)
#
#     await bot.answer_callback_query(call.id)
#     await bot.send_message(call.message.chat.id, f"Новая сделка создается в формате: {text}", reply_markup=markup)
#
# @dispatcher.callback_query_handler(lambda c: c.data == "createClient")
# async def reakcia_na_knopku(call: types.callback_query):
#     markup = InlineKeyboardMarkup()
#     button2 = InlineKeyboardButton("Локация", callback_data="location")
#     button3 = InlineKeyboardButton("Старт сумм", callback_data="button1")
#     button4 = InlineKeyboardButton("Старт валюта", callback_data="button1")
#     button5 = InlineKeyboardButton("Курс", callback_data="button1")
#     button6 = InlineKeyboardButton("Сумма обмена", callback_data="button1")
#     button7 = InlineKeyboardButton("Валюта обмена", callback_data="button1")
#     button8 = InlineKeyboardButton("Способ платежа", callback_data="button1")
#     button9 = InlineKeyboardButton("Контрагент", callback_data="button1")
#     button10 = InlineKeyboardButton("Сбросить все и вернуться в начало", callback_data="NewSdelka")
#     markup.add(button2, button10)
#
#     await bot.answer_callback_query(call.id)
#     await bot.send_message(call.message.chat.id, f"Введите имя клиента в телеграмме через @", reply_markup=markup)




# @dispatcher.callback_query_handler(cb.filter(item_name="startExchange"))
# async def callbacks_num_change_fab(call: types.CallbackQuery, callback_data: dict):
#     print("dsgvs")

if __name__ == '__main__':
    executor.start_polling(dispatcher=dispatcher,
                           skip_updates=True)
