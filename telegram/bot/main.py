import asyncio
import logging
import os
import sqlite3
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from handlers import command_start_handler, button_handler
from keyboards import create_main_keyboard
from config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Подключение к базе данных
conn = sqlite3.connect('bookings.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    username TEXT,
    service TEXT,
    date TEXT,
    time TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')
conn.commit()

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        dp.message.register(command_start_handler, CommandStart())
        dp.message.register(button_handler)
        asyncio.run(main())
    finally:
        conn.close()