from loader import dp, bot
from random import choice
from aiogram import types
from keyboards.default import get_go_kb_one
from utils.states import PlayOne
from loader import db



@dp.callback_query_handler(lambda callback: callback.data.startswith('size_') or callback.data.startswith('random_size'),
                           state=PlayOne.off)
async def cb_size(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.answer()
    db_size = choice((7, 8, 9, 10)) if callback.data == 'random_size' else \
        int(callback.data[callback.data.index('_') + 1:])
    await db.set_game_size(db_size, callback.from_user.id)
    await bot.send_message(chat_id=callback.message.chat.id,
                                   text=f'Вы выбрали размер поля: {db_size}.',
                                   reply_markup=get_go_kb_one())
