from aiogram import Bot, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from googletrans import Translator

from database import sqlite_db
from handlers import addwords, translator

storage = MemoryStorage()
TOKEN = '5912456401:AAGN2IcEcogZa4CF99IJhpD1bAkFtRNpaKg'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

sqlite_db.sqlStart()

detector = Translator()

def wordsToTurple(id, words):
    totalWords = []
    for i in range(0, len(words), 2):
        totalWords.append((id, str(words[i]).capitalize(), str(words[i+1]).capitalize()))
    return (totalWords)

@dp.message_handler(commands=['unlearned'])
async def getAllUnLearnedWords(message: types.Message):
    words = await sqlite_db.sqlGetUnLearnedWords(message.from_user.id)
    for i in words:
        await bot.send_message(message.from_user.id, i)

@dp.message_handler(commands=['learned'])
async def getAllLearnedWords(message: types.Message):
    words = await sqlite_db.sqlGetLearnedWords(message.from_user.id)
    print(words)
    for i in words:
        await bot.send_message(message.from_user.id, i)

@dp.message_handler(commands=['addThis'])
async def getAllLearnedWords(message: types.Message):
    lastTranslatedWord = await sqlite_db.getTranslatedWord(message.from_user.id)
    print(lastTranslatedWord[0][0])
    await sqlite_db.sqlToUnLearned([(message.from_user.id, lastTranslatedWord[0][1], lastTranslatedWord[0][2])])
    await sqlite_db.sqlDeleteWordInTranslated(message.from_user.id)
    await bot.send_message(message.from_user.id, "Added")

# @dp.message_handler()
async def echo_message(message: types.Message, state: FSMContext):
    translate = translator.translate(message.text)
    if translate:
        await bot.send_message(message.from_user.id, translate.text)
        lastTranslatedWord = await sqlite_db.getTranslatedWord(message.from_user.id)
        if (detector.detect(message.text).lang == "en"):
            word = message.text
            translatedWord = translate.text
        else:
            word = translate.text
            translatedWord = message.text
        if (lastTranslatedWord):
            await sqlite_db.sqlUpdateTranslatedWord(id=message.from_user.id, word=word, translate=translatedWord)
        else:
            await sqlite_db.sqlAddTranslatedWord((message.from_user.id, word, translatedWord))



if __name__ == '__main__':
    addwords.reister_handlers_newWords(dp)
    dp.register_message_handler(echo_message)
    executor.start_polling(dp, skip_updates=True)

# db = sqlite3.connect('engltgbot')
#
# cursor = db.cursor()

# cursor.execute("""CREATE TABLE users (
#     login text
# )""")

# cursor.execute("INSERT INTO users VALUES ( 'First Acc' )")

# cursor.execute("SELECT rowid, login FROM users")
# print(cursor.fetchall())
# print(cursor.fetchmany(1)) #[(1, 'First Acc')]
# print(cursor.fetchone()) #(1, 'First Acc')

# logins = cursor.fetchall()
# for login in logins:
    # print(login)

# cursor.execute("DELETE FROM users WHERE login = 'First Acc' ")

# cursor.execute("UPDATE users SET login = 'Second Acc' WHERE login = 'Lol' ")

# cursor.execute("SELECT rowid, login FROM users")
# print(cursor.fetchall())
#
# db.commit()
#
# db.close()