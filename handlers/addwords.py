from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher

from database import sqlite_db
import mainbot

def wordsToTurple(id, words):
    totalWords = []
    for i in range(0, len(words), 2):
        totalWords.append((id, str(words[i]).strip().capitalize(), str(words[i+1]).strip().capitalize()))
    return (totalWords)

class FSMNewWords(StatesGroup):
    newWord = State()

class FSMDeletedWords(StatesGroup):
    DeletedWord = State()

class FSMDeletedWordsInLearned(StatesGroup):
    DeletedWordInLearned = State()

class FSMToLearned(StatesGroup):
    LearnedWord = State()

class FSMToLearnedById(StatesGroup):
    LearnedWordById = State()

class FSMToUnLearned(StatesGroup):
    UnLearnedWord = State()

class FSMToUnLearnedById(StatesGroup):
    UnLearnedWordById = State()

async def startAddingNewWords(message: types.Message):
    await FSMNewWords.newWord.set()
    await message.reply('write Word(s)')


async def addNewWords(message: types.Message, state: FSMContext):
    if(message.text != "/end" and message.text != "/learned" and message.text != "/unlearned"):
        try:
            words = []
            words = message.text.replace(';','-').replace(':','-').replace(',','-').replace('\n','-').split('-')
            if (len(words) % 2 == 0):
                turpleWords = wordsToTurple(id=message.from_user.id, words=words)
                await sqlite_db.sqlAddWordUnLearned(turpleWords)
                await message.reply("Done")
                async with state.proxy() as data:
                    data['newWord'] = message.text
            else:
                await message.reply("You need to write to translates for every word correct!")
        except:
            await message.reply("Error \n For stop write '/end'")
    else:
        await state.finish()
        if (message.text == "/end"):
            await message.reply("Ended Successfully")
        elif (message.text == "/learned"):
            await mainbot.getAllLearnedWords(message)
        elif (message.text == "/unlearned"):
            await mainbot.getAllUnLearnedWords(message)


async def startDeletingWords(message: types.Message):
    await FSMDeletedWords.DeletedWord.set()
    await message.reply('write numbers')

async def DeleteWords(message: types.Message, state: FSMContext):
    if(message.text != "/end" and message.text != "/learned" and message.text != "/unlearned"):
        try:
            TherIsWord = bool(await sqlite_db.getWordByWord(id=message.from_user.id, word=str(message.text).capitalize()))
            await sqlite_db.sqlDeleteWordByWord(id=message.from_user.id, word=str(message.text).capitalize())
            if TherIsWord:
                await message.reply("Deleted!")
                async with state.proxy() as data:
                    data['DeletedWord'] = message.text
            else:
                try:
                    words = await sqlite_db.sqlGetUnLearnedWords(message.from_user.id)
                    word = words[int(message.text)]
                    wordTuple = (message.from_user.id, word[1], word[2])
                    TherIsWord = bool(
                        await sqlite_db.getWordByWord(id=message.from_user.id, word=str(wordTuple[1]).capitalize())
                    )
                    if TherIsWord:
                        await sqlite_db.sqlDeleteWordByWord(id=message.from_user.id, word=str(wordTuple[1]).capitalize())
                        await message.reply("Deleted by id!")
                except:
                    word = await sqlite_db.getWordByTranslate(id=message.from_user.id, word=(str(message.text)).capitalize())
                    print(word)
                    TherIsWord = bool(
                        await sqlite_db.getWordByWord(id=message.from_user.id, word=(str(word[0][1]).capitalize())))
                    print(TherIsWord)
                    if TherIsWord:
                        await sqlite_db.sqlDeleteWordByWord(id=message.from_user.id, word=str(word[0][1]).capitalize())
                        await message.reply("Deleted by Translate!")
                    else:
                        await message.reply("No such word")
        except:
            await message.reply("No Some Word \n For stop write '/end'")
    else:
        await state.finish()
        if (message.text == "/end"):
            await message.reply("Ended Successfully")
        elif (message.text == "/learned"):
            await mainbot.getAllLearnedWords(message)
        elif (message.text == "/unlearned"):
            await mainbot.getAllUnLearnedWords(message)

async def startMoveToLearned(message: types.Message):
    await FSMToLearned.LearnedWord.set()
    await message.reply(await sqlite_db.sqlGetUnLearnedWords(message.from_user.id))
    await message.reply('write Word')

async def MovingToLearned(message: types.Message, state: FSMContext):
    if(message.text != "/end" and message.text != "/learned" and message.text != "/unlearned"):
        try:
            word = await sqlite_db.getWordByWord(id=message.from_user.id, word=str(message.text).capitalize())
            await sqlite_db.sqlDeleteWordByWord(id=message.from_user.id, word=str(message.text).capitalize())
            await sqlite_db.sqlToLearned(word)
            await message.reply("Moved!")
            async with state.proxy() as data:
                data['LearnedWord'] = message.text
        except:
            try:
                try:
                    words = await sqlite_db.sqlGetUnLearnedWords(message.from_user.id)
                    word = words[int(message.text)]
                    wordTuple = (message.from_user.id, word[1], word[2])
                    print(wordTuple)
                    TherIsWord = bool(
                        await sqlite_db.getWordByWord(id=message.from_user.id, word=str(wordTuple[1]).capitalize())
                    )
                    print(TherIsWord)
                    if TherIsWord:
                        await sqlite_db.sqlDeleteWordByWord(id=message.from_user.id,
                                                            word=str(wordTuple[1]).capitalize())
                        await sqlite_db.sqlToLearned([wordTuple])
                        await message.reply("Moved by id!")
                except:
                    word = await sqlite_db.getWordByTranslate(id=message.from_user.id, word=str(message.text).capitalize())
                    await sqlite_db.sqlDeleteWordByWord(id=message.from_user.id, word=str(word[0][1]).capitalize())
                    await sqlite_db.sqlToLearned(word)
                    await message.reply("Moved!")
                    async with state.proxy() as data:
                        data['LearnedWord'] = message.text
            except:
                await message.reply("No Some Word \nFor stop write '/end'")
    else:
        await state.finish()
        if (message.text == "/end"):
            await message.reply("Ended Successfully")
        elif (message.text == "/learned"):
            await mainbot.getAllLearnedWords(message)
        elif (message.text == "/unlearned"):
            await mainbot.getAllUnLearnedWords(message)



# async def startMoveToLearnedById(message: types.Message):
#     await FSMToLearnedById.LearnedWordById.set()
#     await message.reply(await sqlite_db.sqlGetUnLearnedWords(message.from_user.id))
#     await message.reply('write number')

# async def MovingToLearnedById(message: types.Message, state: FSMContext):
#     if(message.text != "/end" and message.text != "/learned" and message.text != "/unlearned"):
#         try:
#             words = await sqlite_db.sqlGetUnLearnedWords(message.from_user.id)
#             word = words[int(message.text)]
#             wordTuple = (message.from_user.id, word[1], word[2])
#             await sqlite_db.sqlDeleteWordByWord(id=message.from_user.id, word=str(wordTuple[1]).capitalize())
#             await sqlite_db.sqlToLearnedById(wordTuple)
#             await message.reply("Moved!")
#             async with state.proxy() as data:
#                 data['LearnedWordById'] = message.text
#         except:
#             await message.reply("No Some Number \n For stop write '/end' ")
#     else:
#         await state.finish()
#         if (message.text == "/end"):
#             await message.reply("Ended Successfully")
#         elif (message.text == "/learned"):
#             await mainbot.getAllLearnedWords(message)
#         elif (message.text == "/unlearned"):
#             await mainbot.getAllUnLearnedWords(message)



async def startMoveToUnLearnedById(message: types.Message):
    await FSMToUnLearnedById.UnLearnedWordById.set()
    await message.reply(await sqlite_db.sqlGetLearnedWords(message.from_user.id))
    await message.reply('write number')

async def MovingToUnLearnedById(message: types.Message, state: FSMContext):
    if(message.text != "/end" and message.text != "/learned" and message.text != "/unlearned"):
        try:
            words = await sqlite_db.sqlGetLearnedWords(message.from_user.id)
            word = words[int(message.text)]
            wordTuple = (message.from_user.id, word[1], word[2])
            await sqlite_db.sqlDeleteLearnedWordByWord(id=message.from_user.id, word=str(wordTuple[1]).capitalize())
            await sqlite_db.sqlToUnLearnedById(wordTuple)
            await message.reply("Moved By Id!")
            async with state.proxy() as data:
                data['LearnedWordById'] = message.text
        except:
            try:
                word = await sqlite_db.getLearnedWordByWord(id=message.from_user.id, word=str(message.text).capitalize())
                if not word:
                    word = await sqlite_db.getLearnedWordByTranslate(id=message.from_user.id, word=str(message.text).capitalize())
                await sqlite_db.sqlDeleteLearnedWordByWord(id=message.from_user.id, word=str(word[0][1]).capitalize())
                await sqlite_db.sqlToUnLearnedById(word[0])
                await message.reply("Moved!")
                async with state.proxy() as data:
                    data['LearnedWordById'] = message.text
            except:
                await message.reply("No Some Number \n For stop write '/end' ")
    else:
        await state.finish()
        if (message.text == "/end"):
            await message.reply("Ended Successfully")
        elif (message.text == "/learned"):
            await mainbot.getAllLearnedWords(message)
        elif (message.text == "/unlearned"):
            await mainbot.getAllUnLearnedWords(message)




async def startDeletingWordsInLearned(message: types.Message):
    await FSMDeletedWordsInLearned.DeletedWordInLearned.set()
    await message.reply('write word which you want to delete')


async def DeleteWordsInLearned(message: types.Message, state: FSMContext):
    if (message.text != "/end" and message.text != "/learned" and message.text != "/unlearned"):
        try:
            TherIsWord = bool(
                await sqlite_db.getLearnedWordByWord(id=message.from_user.id, word=str(message.text).capitalize()))
            if TherIsWord:
                await sqlite_db.sqlDeleteWordByWordInLearned(id=message.from_user.id, word=str(message.text).capitalize())
                await message.reply("Deleted By Word!")
                async with state.proxy() as data:
                    data['DeletedWord'] = message.text
            else:
                word = await sqlite_db.getLearnedWordByTranslate(id=message.from_user.id, word=str(message.text).capitalize())
                if bool(word):
                    print(word)
                    await sqlite_db.sqlDeleteWordByWordInLearned(id=message.from_user.id,
                                                                 word=str(word[0][1]).capitalize())
                    await message.reply("Deleted By Translate!")
                else:
                    try:
                        words = await sqlite_db.sqlGetLearnedWords(message.from_user.id)
                        word = words[int(message.text)]
                        if bool(word):
                            await sqlite_db.sqlDeleteWordByWordInLearned(id=message.from_user.id,
                                                                         word=str(word[1]).capitalize())
                            await message.reply("Deleted By Id!")
                        else:
                            await message.reply("No Some Word \nFor stop write '/end'")
                    except:
                        await message.reply("No Some Word \nFor stop write '/end'")
        except:
            await message.reply("No Some Word \nFor stop write '/end'")
    else:
        await state.finish()
        if (message.text == "/end"):
            await message.reply("Ended Successfully")
        elif (message.text == "/learned"):
            await mainbot.getAllLearnedWords(message)
        elif (message.text == "/unlearned"):
            await mainbot.getAllUnLearnedWords(message)


def reister_handlers_newWords(dp : Dispatcher):
    dp.register_message_handler(startAddingNewWords,commands=['addNewWord'], state=None)
    dp.register_message_handler(addNewWords, state=FSMNewWords.newWord)
    dp.register_message_handler(startDeletingWords, commands=['DeleteWord'], state=None)
    dp.register_message_handler(DeleteWords, state = FSMDeletedWords.DeletedWord) # Done
    dp.register_message_handler(startMoveToLearned, commands=['MoveWord'], state=None)
    dp.register_message_handler(MovingToLearned, state=FSMToLearned.LearnedWord) # Done
    # dp.register_message_handler(startMoveToLearnedById, commands=['MoveWordById'], state=None)
    # dp.register_message_handler(MovingToLearnedById, state=FSMToLearnedById.LearnedWordById)
    dp.register_message_handler(startMoveToUnLearnedById, commands=['MoveWordToUnLearned'], state=None)
    dp.register_message_handler(MovingToUnLearnedById, state=FSMToUnLearnedById.UnLearnedWordById) # Done
    dp.register_message_handler(startDeletingWordsInLearned, commands=['DeleteWordInLearned'], state=None)
    dp.register_message_handler(DeleteWordsInLearned, state=FSMDeletedWordsInLearned.DeletedWordInLearned) #Done