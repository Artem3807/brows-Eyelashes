from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def create_main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="/info")]
        ]
    )
    return keyboard

def create_services_keyboard():
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="Ламинирование ресниц")],
            [KeyboardButton(text="Ламинирование ресниц с окрашиванием")],
            [KeyboardButton(text="Окрашивание бровей с коррекцией")],
            [KeyboardButton(text="Ламинирование бровей с коррекцией + окрашиванием")],
            [KeyboardButton(text="Окрашивание ресниц")],
            [KeyboardButton(text="Назад")]
        ]
    )
    return keyboard

def create_booking_keyboard():
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="Записаться")]
        ]
    )
    return keyboard