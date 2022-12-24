from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from database import sqlite_db
from handlers import addwords

storage = MemoryStorage()
TOKEN = '5912456401:AAGN2IcEcogZa4CF99IJhpD1bAkFtRNpaKg'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

sqlite_db.sqlStart()

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

# @dp.message_handler()
# async def echo_message(message: types.Message):
#         words = []
#         words = message.text.replace(';','-').replace(':','-').replace(',','-').replace('\n','-').strip().split('-')
#         turpleWords = wordsToTurple(id=message.from_user.id, words=words)
#         await sqlite_db.sqlAddCommand(turpleWords)
#         await bot.send_message(message.from_user.id, str(words).strip(']').strip('['))


if __name__ == '__main__':
    addwords.reister_handlers_newWords(dp)
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