from aiogram import executor
from handlers import dp
from loader import db




async def on_startup(_):
    print('Подключение к БД')
    await db.create_table()
    print('Создание таблицы')
    print('Бот запущен!')




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)







