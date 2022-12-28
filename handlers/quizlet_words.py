from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher

from database import sqlite_db
import mainbot

from handlers import parser
from handlers.keyboardd import kb_main, kb_start


def wordsToTurple(id, words):
    totalWords = []
    for i in range(0, len(words), 2):
        totalWords.append((id, str(words[i]).strip().capitalize(), str(words[i+1]).strip().capitalize()))
    return (totalWords)


class FSMQuizletToUnlearned(StatesGroup):
    QuizletWords = State()

async def startAddingQuizlet(message: types.Message):
    await FSMQuizletToUnlearned.QuizletWords.set()
    await message.reply('give me a link of a quizlet', reply_markup=kb_main)

async def AddingQuizletToUnlearned(message: types.Message, state: FSMContext):
    if(message.text != "/end" and message.text != "/learned" and message.text != "/unlearned"):
        try:
            link = message.text
            words = parser.parseQuizlet(url=link)
            for i in range(0, len(words), 2):
                wordsTuple = wordsToTurple(id=message.from_user.id, words=words)
            for i in wordsTuple:
                await sqlite_db.sqlToUnLearned([i])
            await message.reply("Done!")
        except:
            await message.reply("Hmm Wrong link, sory...")
    else:
        await state.finish()
        if (message.text == "/end"):
            await message.reply("Ended Successfully", reply_markup=kb_start)
        elif (message.text == "/learned"):
            await mainbot.getAllLearnedWords(message)
        elif (message.text == "/unlearned"):
            await mainbot.getAllUnLearnedWords(message)


def reister_handlers_newWords(dp : Dispatcher):
    dp.register_message_handler(startAddingQuizlet, commands=['quizlet'], state=None)
    dp.register_message_handler(AddingQuizletToUnlearned, state=FSMQuizletToUnlearned.QuizletWords)