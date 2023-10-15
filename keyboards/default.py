from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_registration():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton('☑️ Регистрация')]],
        resize_keyboard=True, one_time_keyboard=True)

def get_tel_num():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton('📱 Поделиться номером', request_contact=True)],
    [KeyboardButton('Пропустить')]],
        resize_keyboard=True, one_time_keyboard=True)


def main_menu_kb():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text='⛴ Одиночная игра')],
        [KeyboardButton(text='🚢 Мультиплеер')]
    ], resize_keyboard = True)



def get_go_kb():
    return ReplyKeyboardMarkup(keyboard = [
        [KeyboardButton('🎮 Начать игру'), KeyboardButton('❓ Справка')],
        [KeyboardButton('📐 Изменить размер поля'), KeyboardButton('👤 Изменить аватар')],
        [KeyboardButton(text='🏠 Главное меню'),KeyboardButton(text='🔎 Найти игрока')]

    ], resize_keyboard=True)

def get_go_kb_one():
    return ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton('🎮 Начать игру'), KeyboardButton('❓ Справка')],
        [KeyboardButton('📐 Изменить размер поля'), KeyboardButton('👤 Изменить аватар')],
        [KeyboardButton(text='🏠 Главное меню')]
    ], resize_keyboard=True)

def get_cancel_kb():
    return ReplyKeyboardMarkup(keyboard = [
        [KeyboardButton('❌ Выйти из игры')]
    ], resize_keyboard=True)


