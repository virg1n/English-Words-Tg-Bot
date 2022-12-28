from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

unlearnedButton = KeyboardButton('/unlearned')
learnedButton = KeyboardButton('/learned')
quizletButton = KeyboardButton('/quizlet')
addInUnlearnedButton = KeyboardButton('/addNewWord')
deleteInUnlearnedButton = KeyboardButton('/DeleteWord')
moveToLearnedButton = KeyboardButton('/MoveWord')
deleteInlearnedButton = KeyboardButton('/DeleteWordInLearned')
moveToUnLearnedButton = KeyboardButton('/MoveWordToUnLearned')
endButton = KeyboardButton('/end')



kb_start = ReplyKeyboardMarkup(resize_keyboard=True) #, one_time_keyboard=True

kb_main = ReplyKeyboardMarkup(resize_keyboard=True)

kb_unlearned = ReplyKeyboardMarkup(resize_keyboard=True)

kb_learned = ReplyKeyboardMarkup(resize_keyboard=True)



# kb.add(button1).insert(button2).add(button3)
kb_start.row(unlearnedButton, learnedButton).row(addInUnlearnedButton, quizletButton)
kb_main.row(unlearnedButton, learnedButton).add(endButton)
kb_unlearned.row(learnedButton, quizletButton).row(addInUnlearnedButton, deleteInUnlearnedButton, moveToLearnedButton)
kb_learned.row(unlearnedButton, quizletButton).row(addInUnlearnedButton, deleteInlearnedButton, moveToUnLearnedButton)