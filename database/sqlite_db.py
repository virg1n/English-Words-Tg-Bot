import sqlite3 as sq

def sqlStart():
    global base, cur
    base = sq.connect('englwords.db')
    cur = base.cursor()
    if base:
        print("DB connected")
    # base.execute('CREATE TABLE IF NOT EXISTS users(user_id TEXT, word TEXT, translate TEXT)')
    base.execute('CREATE TABLE IF NOT EXISTS learned(user_id TEXT, word TEXT, translate TEXT)')
    base.execute('CREATE TABLE IF NOT EXISTS unlearned(user_id TEXT, word TEXT, translate TEXT)')
    base.execute('CREATE TABLE IF NOT EXISTS addTranslatedWord(user_id TEXT, word TEXT, translate TEXT)')
    base.commit()

async def sqlAddCommand(words):
    for i in words:
        cur.execute('INSERT INTO users VALUES(?, ?, ?)', tuple(i))
    base.commit()
    # cur.execute("SELECT word, translate FROM words")
    # print(cur.fetchall())

async def sqlGetUnLearnedWords(user_id):
    cur.execute("SELECT word, translate FROM unlearned WHERE user_id=={}".format(user_id))
    words = cur.fetchall()
    for i in range(len(words)):
        words[i] = (i, ) + words[i]
    return(words)

async def sqlGetLearnedWords(user_id):
    cur.execute("SELECT word, translate FROM learned WHERE user_id=={}".format(user_id))
    words = cur.fetchall()
    for i in range(len(words)):
        words[i] = (i,) + words[i]
    return(words)

async def sqlDeleteWordByWord(id, word):
    cur.execute("DELETE FROM unlearned WHERE word=='{}' AND user_id='{}' ".format(word, id))
    base.commit()

async def sqlDeleteWordByWordInLearned(id, word):
    cur.execute("DELETE FROM learned WHERE word=='{}' AND user_id='{}' ".format(word, id))
    base.commit()

async def getWordByWord(id, word):
    return (cur.execute("SELECT * FROM unlearned WHERE word=='{}' AND user_id='{}'".format(word, id)).fetchall())

async def getWordByTranslate(id, word):
    return (cur.execute("SELECT * FROM unlearned WHERE translate=='{}' AND user_id='{}'".format(word, id)).fetchall())

async def getLearnedWordByWord(id, word):
    return (cur.execute("SELECT * FROM learned WHERE word=='{}' AND user_id='{}'".format(word, id)).fetchall())

async def getLearnedWordByTranslate(id, word):
    return (cur.execute("SELECT * FROM learned WHERE translate=='{}' AND user_id='{}'".format(word, id)).fetchall())

async def sqlToLearned(word):
    cur.execute('INSERT INTO learned VALUES(?, ?, ?)', tuple(word[0]))
    base.commit()

async def sqlToLearnedById(word):
    cur.execute('INSERT INTO learned VALUES(?, ?, ?)', tuple(word))
    base.commit()

async def sqlToUnLearned(word):
    cur.execute('INSERT INTO unlearned VALUES(?, ?, ?)', tuple(word[0]))
    base.commit()

async def sqlToUnLearnedById(word):
    cur.execute('INSERT INTO unlearned VALUES(?, ?, ?)', tuple(word))
    base.commit()

async def sqlDeleteLearnedWordByWord(id, word):
    cur.execute("DELETE FROM learned WHERE word=='{}' AND user_id='{}' ".format(word, id))
    base.commit()

async def getLearnedWordByWord(id, word):
    return (cur.execute("SELECT * FROM learned WHERE word=='{}' AND user_id='{}'".format(word, id)).fetchall())

async def sqlDeleteWordByNumber(id, number):
    cur.execute("DELETE FROM unlearned WHERE word=='{}' AND user_id='{}' ".format(number, id))
    base.commit()

async def sqlAddWordUnLearned(words):
    for i in words:
        cur.execute('INSERT INTO unlearned VALUES(?, ?, ?)', tuple(i))
    base.commit()

async def sqlAddWordLearned(words):
    for i in words:
        cur.execute('INSERT INTO learned VALUES(?, ?, ?)', tuple(i))
    base.commit()

async def sqlAddTranslatedWord(word):
    cur.execute('INSERT INTO addTranslatedWord VALUES(?, ?, ?)', word)
    base.commit()

async def sqlUpdateTranslatedWord(word, translate, id):
    cur.execute('UPDATE addTranslatedWord SET word="{}", translate="{}" WHERE user_id="{}"'.format(word, translate, id))
    base.commit()

async def getTranslatedWord(id):
    return (cur.execute("SELECT * FROM addTranslatedWord WHERE user_id='{}'".format(id)).fetchall())

async def sqlDeleteWordInTranslated(id):
    cur.execute("DELETE FROM addTranslatedWord WHERE user_id=='{}' ".format( id))
    base.commit()
