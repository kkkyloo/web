import requests
import key as nav
import asyncio
import datetime

from config import tg_bot_token, open_weather_token
from aiogram.dispatcher import Dispatcher
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from db import Database

bot = Bot(token=tg_bot_token)
dp = Dispatcher(bot, storage=MemoryStorage())
db = Database('base.db')

class Form(StatesGroup):
    city = State() 
    city_change = State() 

@dp.message_handler(commands=['start'])
async def change_language(message: types.Message):
    if message.chat.type == 'private':
        if not db.user_exists(message.from_user.id):
            await bot.send_message(message.from_user.id, f"Здраствуйте, {message.from_user.username}, выберете язык:", reply_markup = nav.first_menu)
        else:
            if db.read_isru() == 1:
                await bot.send_message(message.from_user.id, f"Добро пожаловать обратно, {message.from_user.username} \nВыберите действие на кнопках:", reply_markup = nav.rus_menu)
            else:
                await bot.send_message(message.from_user.id, f"Welcome back, {message.from_user.username} \nChoose an action on the buttons:", reply_markup = nav.eng_menu)


@dp.message_handler()
async def send_menu(message: types.Message):
    match message.text:
        case "Русский":
            db.add_isru(message.from_user.id, 1)
            await Form.city.set()
            await bot.send_message(message.from_user.id, f"Введите город:", reply_markup=types.ReplyKeyboardRemove())
        case "Погода сейчас":
            await bot.send_message(message.from_user.id, weather_now("ru", db.read_sqlite_table()))
        case "Weather now":
            await bot.send_message(message.from_user.id, weather_now("en", db.read_sqlite_table()))            
        case "Погода на завтра":
            await bot.send_message(message.from_user.id, weather_tom("ru",db.read_sqlite_table()))
        case "Weather tomorrow":
            await bot.send_message(message.from_user.id, weather_tom("en",db.read_sqlite_table()))
        case "Погода на 5 дней":
            await bot.send_message(message.from_user.id, weather_five("ru",db.read_sqlite_table()))
        case "Weather for 5 days":
            await bot.send_message(message.from_user.id, weather_five("en",db.read_sqlite_table()))
        case "Сменить город":
            await Form.city_change.set()
            await bot.send_message(message.from_user.id, f"Введите город:")
        case "Change city":
            await Form.city_change.set()
            await bot.send_message(message.from_user.id, f"Send city:")            
        case "Уведомления":
            if db.read_push() == 0:
                await bot.send_message(message.from_user.id, "Выберете настройки уведомлений", reply_markup = nav.push_menu1)
            else:
                await bot.send_message(message.from_user.id, "Выберете настройки уведомлений",reply_markup = nav.push_menu2)
        case "Notifications":
            if db.read_push() == 0:
                await bot.send_message(message.from_user.id, "Choose notification settings", reply_markup = nav.push_menu3) 
            else:
                await bot.send_message(message.from_user.id, "Choose notification settings",reply_markup = nav.push_menu4)
        case "Включить уведомления":
            db.update_bool(message.from_user.id, True)
            dt = datetime.datetime.today()
            await bot.send_message(message.from_user.id, f"Уведомления включены на 07:00", reply_markup = nav.rus_menu)
            while db.read_push() == 1:
                await asyncio.sleep(abs(int(dt.hour) - 7)*3600 - 60 * int(dt.minute))
                await message.reply(weather_now(db.read_sqlite_table()))
        case "Enable Notifications":
            db.update_bool(message.from_user.id, True)
            dt = datetime.datetime.today()
            await bot.send_message(message.from_user.id, f"Notifications enabled at 07:00", reply_markup = nav.eng_menu)
            while db.read_push() == 1:
                await asyncio.sleep(abs(int(dt.hour) - 7)*3600 - 60 * int(dt.minute))
                await message.reply(weather_now(db.read_sqlite_table()))
        case "Вернуться":
            await bot.send_message(message.from_user.id, "Выберите действие на кнопках", reply_markup = nav.rus_menu)
        case "Back":
            await bot.send_message(message.from_user.id, "Choose an action on the buttons", reply_markup = nav.eng_menu)
        case "Отключить уведомления":
            db.update_bool(message.from_user.id, False)
            await bot.send_message(message.from_user.id, f"Уведомления отключены", reply_markup = nav.rus_menu)
        case "Disable Notifications":
            db.update_bool(message.from_user.id, False)
            await bot.send_message(message.from_user.id, f"Notifications disabled", reply_markup = nav.eng_menu)
        case "English":
            db.add_isru(message.from_user.id, 0)
            await Form.city.set()
            await bot.send_message(message.from_user.id, f"Send city:", reply_markup=types.ReplyKeyboardRemove())
        case "Сменить язык на английский":
            db.update_isru(message.from_user.id, 0)
            await bot.send_message(message.from_user.id, f"Your city {db.read_sqlite_table()}. \nSelect action on button", reply_markup = nav.eng_menu)
        case "Change language to Rus":
            db.update_isru(message.from_user.id, 1)
            await bot.send_message(message.from_user.id, f"Вами выбран город {db.read_sqlite_table()}. \nВыберите действие на кнопках", reply_markup = nav.rus_menu)

@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()

@dp.message_handler(state=Form.city)
async def process_city(message: types.Message, state: FSMContext):
        if db.read_isru() == 1:
            try:
                r = requests.get(
                    f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric&lang=ru"
                )        
                data = r.json()
                city = data["name"]

                db.update_sqlite_table2(message.text, message.from_user.id)   
                await bot.send_message(message.from_user.id, f"Вами выбран город {message.text}. \nВыберите действие на кнопках", reply_markup = nav.rus_menu)

                await state.finish()

            except:
                await message.reply("Город не найден, попробуйте ещё раз")
        else:
            try:
                r = requests.get(
                        f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric&lang=ru"
                    )        
                data = r.json()
                city = data["name"]

                db.update_sqlite_table2(message.text, message.from_user.id) 
                await bot.send_message(message.from_user.id, f"Your city {message.text}. \nSelect action on button", reply_markup = nav.eng_menu)

                await state.finish()

            except:
                await message.reply("City not found, please try again")

@dp.message_handler(state=Form.city_change)
async def process_city(message: types.Message, state: FSMContext):
    try:    
        if db.read_isru() == 1:
            r = requests.get(
                f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric&lang=ru"
            )    
            data = r.json()
            city = data["name"]
            db.update_sqlite_table(message.from_user.id, message.text)

            await bot.send_message(message.from_user.id, f"Вами выбран город {message.text}. \nВыберите действие на кнопках", reply_markup = nav.rus_menu)

            await state.finish()

        else:
            r = requests.get(
                f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={open_weather_token}&units=metric&lang=en"
            )    
            data = r.json()
            city = data["name"]
            db.update_sqlite_table(message.from_user.id, message.text)

            await bot.send_message(message.from_user.id, f"You choosed {message.text}. \nChoose an action on the buttons", reply_markup = nav.eng_menu)

            await state.finish()

    except:
        await message.reply("Город не найден, попробуйте ещё раз")

def weather_now(lang, x):
    r = requests.get(
        f"http://api.openweathermap.org/data/2.5/weather?q={x}&appid={open_weather_token}&units=metric&lang={lang}"
    )
    data = r.json()

    
    city = data["name"]
    weather = data["weather"][0]['description']
    cur_weather = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    wind = data["wind"]["speed"]

    if lang == "ru":
        return str(f"Погода в городе {city} - {weather}\nТемпература: {cur_weather}C°\nОщущается: {feels_like}C°\n"
            f"Влажность: {humidity}%\nВетер: {wind} м/с\n"
            )
    else:
        return str(f"City weather {city} - {weather}\nTemperature: {cur_weather}C°\nFeels like: {feels_like}C°\n"
            f"Humidity: {humidity}%\nWind: {wind} м/с\n"
            )

def weather_tom(lang,x):
    print(x)
    r = requests.get(
        f"http://api.openweathermap.org/data/2.5/forecast?q={x}&appid={open_weather_token}&units=metric&lang={lang}"
    )
    data = r.json()

    city = data["city"]['name']

    day1 = data["list"][8]['dt_txt']
    temp1 = data["list"][8]['main']["temp"]
    wind1 = data["list"][8]['wind']["speed"]
    weather = data["list"][8]['weather'][0]["description"]
    feels_like = data["list"][8]['main']["feels_like"]
    humidity = data["list"][8]['main']["humidity"]
    

    if lang == "ru":
        return str(
            f"Погода в городе {city} на {day1[:10]}: \n{weather}°\n"
            f"Температура: {temp1}C°\n"
            f"Ощущается: {feels_like}C°\n"
            f"Влажность: {humidity}%\n"
            f"Ветер: {wind1} м/с\n"
            )

    else:
        return str(
            f"City weather {city} {day1[:10]}: \n{weather}°\n"
            f"Temperature: {temp1}C°\n"
            f"Feels like: {feels_like}C°\n"
            f"Humidity: {humidity}%\n"
            f"Wind1: {wind1} м/с\n"
            )        

def weather_five(lang,x):
    print(x)
    r = requests.get(
        f"http://api.openweathermap.org/data/2.5/forecast?q={x}&appid={open_weather_token}&units=metric&lang={lang}"
    )
    data = r.json()

    
    city = data["city"]['name']

    day1 = data["list"][4]['dt_txt']
    temp1 = data["list"][4]['main']["temp"]
    wind1 = data["list"][4]['wind']["speed"]
    weather1 = data["list"][4]['weather'][0]["description"]
    feels_like1 = data["list"][4]['main']["feels_like"]
    humidity1 = data["list"][4]['main']["humidity"]

    day2 = data["list"][12]['dt_txt']
    temp2 = data["list"][12]['main']["temp"]
    wind2 = data["list"][12]['wind']["speed"]
    weather2 = data["list"][12]['weather'][0]["description"]
    feels_like2 = data["list"][12]['main']["feels_like"]
    humidity2 = data["list"][12]['main']["humidity"]

    day3 = data["list"][20]['dt_txt']
    temp3 = data["list"][20]['main']["temp"]
    wind3 = data["list"][20]['wind']["speed"]
    weather3 = data["list"][20]['weather'][0]["description"]
    feels_like3 = data["list"][20]['main']["feels_like"]
    humidity3 = data["list"][20]['main']["humidity"]

    day4 = data["list"][28]['dt_txt']
    temp4 = data["list"][28]['main']["temp"]
    wind4 = data["list"][28]['wind']["speed"]
    weather4 = data["list"][28]['weather'][0]["description"]
    feels_like4 = data["list"][28]['main']["feels_like"]
    humidity4 = data["list"][28]['main']["humidity"]

    day5 = data["list"][36]['dt_txt']
    temp5 = data["list"][36]['main']["temp"]
    wind5 = data["list"][36]['wind']["speed"]
    weather5 = data["list"][36]['weather'][0]["description"]
    feels_like5 = data["list"][36]['main']["feels_like"]
    humidity5 = data["list"][36]['main']["humidity"]

    if lang == "ru":
        return str(
            f"Погода в городе {city} на {day1[:10]}: \n{weather1}°\n"
            f"Температура: {temp1}C°\n"
            f"Ощущается: {feels_like1}C°\n"
            f"Влажность: {humidity1}%\n"
            f"Ветер: {wind1} м/с\n"

            f"\nПогода в городе {city} на {day2[:10]}: \n{weather2}°\n"
            f"Температура: {temp2}C°\n"
            f"Ощущается: {feels_like2}C°\n"
            f"Влажность: {humidity2}%\n"
            f"Ветер: {wind2} м/с\n"

            f"\nПогода в городе {city} на {day3[:10]}: \n{weather3}°\n"
            f"Температура: {temp3}C°\n"
            f"Ощущается: {feels_like3}C°\n"
            f"Влажность: {humidity3}%\n"
            f"Ветер: {wind3} м/с\n"
            
            f"\nПогода в городе {city} на {day4[:10]}: \n{weather4}°\n"
            f"Температура: {temp4}C°\n"
            f"Ощущается: {feels_like4}C°\n"
            f"Влажность: {humidity4}%\n"
            f"Ветер: {wind4} м/с\n"

            f"\nПогода в городе {city} на {day5[:10]}: \n{weather5}°\n"
            f"Температура: {temp5}C°\n"
            f"Ощущается: {feels_like5}C°\n"
            f"Влажность: {humidity5}%\n"
            f"Ветер: {wind5} м/с\n"
            )
    else:
        return str(
            f"City weather {city} {day1[:10]}: \n{weather1}°\n"
            f"Temperature: {temp1}C°\n"
            f"Feels like: {feels_like1}C°\n"
            f"Humidity: {humidity1}%\n"
            f"Wind: {wind1} м/с\n"

            f"\nCity weather {city} {day2[:10]}: \n{weather2}°\n"
            f"Temperature: {temp2}C°\n"
            f"Feels like: {feels_like2}C°\n"
            f"Humidity: {humidity2}%\n"
            f"Wind: {wind2} м/с\n"

            f"\nCity weather {city} {day3[:10]}: \n{weather3}°\n"
            f"Temperature: {temp3}C°\n"
            f"Feels like: {feels_like3}C°\n"
            f"Humidity: {humidity3}%\n"
            f"Wind: {wind3} м/с\n"
            
            f"\nCity weather {city} {day4[:10]}: \n{weather4}°\n"
            f"Temperature: {temp4}C°\n"
            f"Feels like: {feels_like4}C°\n"
            f"Humidity: {humidity4}%\n"
            f"Wind: {wind4} м/с\n"

            f"\nПогода в городе {city} {day5[:10]}: \n{weather5}°\n"
            f"Temperature: {temp5}C°\n"
            f"Feels like: {feels_like5}C°\n"
            f"Humidity: {humidity5}%\n"
            f"Wind: {wind5} м/с\n"
            )       

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)