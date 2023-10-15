
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData


choose_callback = CallbackData('choose','player_id')
send_game = CallbackData('send_game','game')
take_game = CallbackData('take_game','game')



def get_choice_ikb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Выбрать аватар', callback_data='choice')],
        [InlineKeyboardButton('Случайный аватар', callback_data='random_choice')]
    ])


def get_size_ikb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('7', callback_data='size_7'),InlineKeyboardButton('8', callback_data='size_8')],
        [InlineKeyboardButton('9', callback_data='size_9'), InlineKeyboardButton('10', callback_data='size_10')],
        [InlineKeyboardButton('Случайный выбор', callback_data='random_size')]

    ])

def get_next_choice_ikb():
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('⬅️', callback_data='prev'), InlineKeyboardButton('➡️', callback_data='next')],
        [InlineKeyboardButton('✅ Выбрать', callback_data='set_it')]

    ])
    return ikb

def choose_player(player_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Выбрать', callback_data=choose_callback.new(player_id=player_id))]
    ])

def offer(opponent_id):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Присоедениться', callback_data=f'yes_{opponent_id}')],
        [InlineKeyboardButton('Отказаться', callback_data=f'no_{opponent_id}')]
    ])


