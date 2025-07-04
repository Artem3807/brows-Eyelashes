from aiogram.types import Message
from keyboards import create_main_keyboard, create_services_keyboard, create_booking_keyboard
from aiogram.types import FSInputFile
from datetime import datetime
import os

user_states = {}

async def command_start_handler(message: Message):
    await message.answer("Привет! Выбери действие:", reply_markup=create_main_keyboard())

async def button_handler(message: Message):
    user_id = message.from_user.id
    if message.text == "/info":
        info_text = "Это информационное сообщение!"
        await message.answer(info_text, reply_markup=create_services_keyboard())
    elif message.text in ["Ламинирование ресниц", "Ламинирование ресниц с окрашиванием", "Окрашивание бровей с коррекцией",
                          "Ламинирование бровей с коррекцией + окрашиванием", "Окрашивание ресниц"]:
        user_states[user_id] = {"service": message.text}
        service_texts = {
            "Ламинирование ресниц": """Ламинирование ресниц — это процедура, придающая естественным ресницам изгиб, объем и насыщенный цвет. Состав на основе кератина питает и укрепляет ресницы, создавая эффект распахнутого взгляда на несколько недель.
Стоимость: 1000 р.""",
            "Ламинирование ресниц с окрашиванием": """Ламинирование ресниц с окрашиванием — это процедура, которая помогает создать эффект длинных, объемных и ухоженных ресниц.
В процессе ламинирования используются специальные составы, которые укрепляют и придают форму ресницам, а также окрашивание, которое придаёт им насыщенный цвет.
Результат сохраняется до 6-8 недель, делая взгляд более выразительным и ярким без необходимости использования туши.
Процедура безопасна и подходит для большинства типов ресниц.
Стоимость: 1200 р.""",
            "Окрашивание бровей с коррекцией": """Окрашивание бровей + коррекция — это косметическая процедура, направленная на придание бровям насыщенного цвета и четкой формы.
С помощью специальных красителей можно скорректировать цвет бровей, сделать их более яркими и выразительными, а также скрыть редкие или светлые волоски.
Стоимость: 700 р.""",
            "Ламинирование бровей с коррекцией + окрашиванием": """Ламинирование бровей + коррекция + окрашивание — это процедура, которая помогает создать эффект ухоженных и объемных бровей.
Во время ламинирования волосы бровей укладываются в нужном направлении и фиксируются специальным составом, что придает им форму и блеск.
Эта процедура также питает и укрепляет волосы, делая их более здоровыми.
Стоимость: 1100 р.""",
            "Окрашивание ресниц": """Окрашивание ресниц — это косметическая процедура, при которой ресницы окрашиваются специальными безопасными красителями.
Эта услуга помогает сделать ресницы более выразительными, придавая им насыщенный цвет и видимость объема.
Окрашивание подходит для светлых или редких ресниц, позволяя избежать использования туши и облегчая ежедневный макияж
Стоимость: 500 р."""
        }
        photo_paths = {
            "Ламинирование ресниц": 'model1.jpg',
            "Ламинирование ресниц с окрашиванием": 'model2.jpg',
            "Окрашивание бровей с коррекцией": 'model3.jpg',
            "Ламинирование бровей с коррекцией + окрашиванием": 'model4.jpg',
            "Окрашивание ресниц": 'model5.jpg'
        }
        photo_path = os.path.join('media', photo_paths[message.text])
        photo = FSInputFile(photo_path)
        await message.answer_photo(photo, caption=service_texts[message.text], reply_markup=create_booking_keyboard())
    elif message.text == "Записаться":
        user_states[user_id] = {"awaiting": "date", "service": user_states.get(user_id, {}).get("service")}
        await message.answer("Пожалуйста, введите дату записи в формате ДД.ММ.ГГГГ:")
    elif user_id in user_states and user_states[user_id].get("awaiting") == "date":
        try:
            date = datetime.strptime(message.text, "%d.%m.%Y").date()
            user_states[user_id]["date"] = date.strftime("%d.%m.%Y")
            user_states[user_id]["awaiting"] = "time"
            await message.answer("Теперь введите время в формате ЧЧ:ММ:")
        except ValueError:
            await message.answer("Неверный формат даты. Пожалуйста, введите дату в формате ДД.ММ.ГГГГ:")
    elif user_id in user_states and user_states[user_id].get("awaiting") == "time":
        try:
            time = datetime.strptime(message.text, "%H:%M").time()
            user_states[user_id]["time"] = time.strftime("%H:%M")
            service = user_states[user_id]["service"]
            date = user_states[user_id]["date"]
            time_str = user_states[user_id]["time"]

            from main import cursor, conn
            cursor.execute('INSERT INTO bookings (user_id, username, service, date, time) VALUES (?, ?, ?, ?, ?)',
                          (user_id, message.from_user.username, service, date, time_str))
            conn.commit()

            await message.answer(f"Вы успешно записаны на услугу {service} на {date} в {time_str}!", reply_markup=create_services_keyboard())
            user_states.pop(user_id, None)
        except ValueError:
            await message.answer("Неверный формат времени. Пожалуйста, введите время в формате ЧЧ:ММ:")
    elif message.text == "Назад":
        await message.answer("Вы вернулись в главное меню", reply_markup=create_main_keyboard())
    else:
        await message.answer("Неизвестная кнопка")