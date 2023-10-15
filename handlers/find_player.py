from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from loader import db
from utils.states import PlayOne
from loader import dp, bot
from aiogram import types
from keyboards.default import get_go_kb
from keyboards.inline import get_choice_ikb, choose_player, choose_callback, offer


@dp.message_handler(text ='🔎 Найти игрока')
async def find_player(message: types.Message):
    user_id = message.from_user.id
    await db.set_status(user_id, 'off')
    await db.set_game_size(0, user_id)
    await db.set_opponent(user_id)
    if not (await db.get_avatar(user_id))[0]:
        return await message.answer(text='Чтобы начать новую игру, выберите аватар.',
                                    reply_markup=get_choice_ikb())
    users = await db.get_all_users(user_id)
    users = [user for user in users if user[10] == 'off']
    await message.answer(f'{message.from_user.full_name}, выберите, с кем хотите сыграть')
    if not users:
        await message.answer('Пока что игроков нету')
        return
    for user in users:
        await message.answer(f'@{user[2]}', reply_markup=choose_player(user[0]))




@dp.callback_query_handler(choose_callback.filter())
async def select_player (callback: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await callback.answer()
    player_id = callback.from_user.id
    username = callback.from_user.username
    async with state.proxy() as data:
        data['opponent_id'] = int(callback_data.get('player_id'))
        data['opponent_name'] = (await db.get_user(data['opponent_id']))[2]
        await bot.send_message(chat_id = data['opponent_id'], text=f"Пользователь {username} "
                                                                f"предлагает вам сыграть.",
                               reply_markup = offer(str(player_id)))



@dp.callback_query_handler(Text(startswith='yes_'), state=[None, PlayOne.off])
async def select_player (callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await state.finish()
    player_id = callback.from_user.id
    username = callback.from_user.username
    async with state.proxy() as data:
        data['opponent_id'] = int(callback.data[callback.data.find('_')+1:])
        data['opponent_name'] = (await db.get_user(data['opponent_id']))[2]
        await db.set_opponent(player_id, data['opponent_id'])
        await callback.message.answer("Вы приняли предложение сыграть.",
                                      reply_markup = get_go_kb())
        await bot.send_message(chat_id=data['opponent_id'], text=f"Пользователь @{username} "
                                                              f"принял ваше предложение.",)

@dp.callback_query_handler(Text(startswith='no_'), state=[None, PlayOne.off])
async def no_play (callback: types.CallbackQuery):
    await callback.answer()
    opponent_id = int(callback.data[callback.data.find('_')+1:])
    await callback.message.answer("Вы отказались от игры.")
    await bot.send_message(chat_id = opponent_id, text=f"Пользователь @{callback.from_user.username} "
                                                                f"отклонил ваше предложение.")


