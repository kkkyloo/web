from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btn_main = KeyboardButton("Вернуться")
btn_main2 = KeyboardButton("Back")

#main

btn_rus = KeyboardButton("Русский")
btn_eng = KeyboardButton("English")
first_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_rus, btn_eng)


# rus

btn_now = KeyboardButton("Погода сейчас")
btn_tom = KeyboardButton("Погода на завтра")
btn_ten = KeyboardButton("Погода на 5 дней")
btn_push = KeyboardButton("Уведомления")
btn_change = KeyboardButton("Сменить город")
btn_lang = KeyboardButton("Сменить язык на английский")
rus_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_now, btn_tom, btn_ten, btn_push, btn_change, btn_lang)

# eng

btn_now = KeyboardButton("Weather now")
btn_tom = KeyboardButton("Weather tomorrow")
btn_ten = KeyboardButton("Weather for 5 days")
btn_push = KeyboardButton("Notifications")
btn_change = KeyboardButton("Change city")
btn_lang = KeyboardButton("Change language to Rus")

eng_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_now, btn_tom, btn_ten, btn_push,btn_change, btn_lang)

# push , reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

btn_ena =  KeyboardButton("Включить уведомления")
btn_dis =  KeyboardButton("Отключить уведомления")
push_menu1 = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_ena, btn_main)
push_menu2 = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_dis, btn_main)

btn_ena =  KeyboardButton("Enable Notifications")
btn_dis =  KeyboardButton("Disable Notifications")
push_menu3 = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_ena, btn_main2)
push_menu4 = ReplyKeyboardMarkup(resize_keyboard=True).add(btn_dis, btn_main2)





