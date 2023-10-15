from loader import dp, bot
from random import choice
from aiogram import types
from keyboards.default import get_go_kb
from loader import db


@dp.callback_query_handler(lambda callback: callback.data.startswith('size_') or callback.data.startswith('random_size'))
async def cb_size(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.answer()
    db_size = choice ((7,8,9,10)) if callback.data=='random_size' else\
        int(callback.data[callback.data.index('_')+1:])
    opponent = await db.get_opponent(callback.from_user.id)
    if opponent:
        status_op = await db.get_status(opponent)
        if status_op != 'active':
            await db.set_game_size(db_size, callback.from_user.id)
            await db.set_game_size(db_size, opponent)
            await bot.send_message(chat_id=callback.message.chat.id,
                                   text=f'Вы выбрали размер поля: {db_size}.',
                                   reply_markup=get_go_kb())
        else:
            db_size = await db.get_game_size(opponent)
            opponent_name = (await db.get_user(opponent))[2]
            return await callback.message.answer(text = f'Игрок @{opponent_name} уже выбрал'
                                                            f' размер игрового поля - <b>{db_size}</b>.')
    else:
        await bot.send_message(chat_id=callback.message.chat.id,
                               text=f'Найдите соперника перед тем, как выбрать размер поля.',
                               reply_markup=get_go_kb())

