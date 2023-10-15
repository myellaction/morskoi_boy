from loader import dp, bot
import asyncio
from random import choice
from aiogram.types import ChatActions
from aiogram.dispatcher import FSMContext
from data import StartGame
from aiogram import types
from keyboards.default import get_cancel_kb, get_go_kb
from utils.states import GameStatesGroup
from loader import db


@dp.message_handler(text='🎮 Начать игру')
async def cmd_go(message: types.Message, state: FSMContext):
    await message.delete()
    player_id = message.from_user.id
    opponent_id = await db.get_opponent(player_id)
    if not opponent_id:
        return await message.answer(text='Вы не выбрали соперника.')
    maybe_opponent = await db.get_opponent(opponent_id)
    if maybe_opponent != player_id:
        username_op = (await db.get_user(opponent_id))[2]
        return await message.answer(text=f'Оппонент @{username_op} не добавлен в вашу игру.')
    step_op = await db.get_step(opponent_id)
    if not step_op or step_op == 'opponent':
        await db.set_step(player_id, 'you')
    else:
        await db.set_step(player_id, 'opponent')
    step_us = await db.get_step(player_id)
    db_size = await db.get_game_size(player_id)
    db_size_op = await db.get_game_size(opponent_id)
    equal = db_size == db_size_op
    if not equal:
        return await message.answer(text = 'Размер вашего поля отличается от оппонента.\n'
                                           '⚠️ <b>Измените размер поля.</b>')
    await GameStatesGroup.play.set()
    await db.set_status(player_id, 'active')
    async with state.proxy() as data:
        if db_size:
            data['game'] = StartGame(db_size)

        else:
            db_size = choice(range(7,11))
            data['game'] = StartGame(db_size)
            await db.set_game_size(db_size, player_id)
            await db.set_game_size(db_size, opponent_id)

        my_pole = data['game'].user.get_pole()
        my_pole = ','.join([' '.join([str(i) for i in j]) for j in my_pole])
        await db.set_pole(pole=my_pole, player_id=player_id, opponent_id=opponent_id)
        if step_us == 'you':
            await message.answer(f"Рыба - карась, игра началась! Ваш ход.\nВведите два числа через пробел, от 1 до {db_size}.",
                         reply_markup=get_cancel_kb())
        else:
            await message.answer(
                f"Рыба - карась, игра началась!\n"
                f"Размер игрового поля - {db_size}\n"
                f"<b>Сейчас ход соперника.</b>",
                reply_markup=get_cancel_kb())



@dp.message_handler(lambda message: len(message.text.split())==2
                    and all([ i.isdigit() and 1<=int(i)<=10 for i in message.text.split()]), state = GameStatesGroup.play)
async def computer_step(message: types.Message, state: FSMContext):

    x, y = message.text.split()
    player_id = message.from_user.id
    opponent_id = await db.get_opponent(player_id)
    if not opponent_id:
        return await message.answer(text='Ваш соперник в другой игре.')
    opponent_status = await db.get_status(opponent_id)
    if opponent_status == 'off':
        return await message.answer(f'<b>Ваш соперник не в игре.</b>\n'
                             f'Выйдите из игры 👇, чтобы начать новую.\n'
                             f'🕰 Или <b>дождитесь</b>, пока он зайдет.')


    step_us = await db.get_step(player_id)
    if step_us != 'you':
        return await message.answer('Сейчас ход соперника.\n<b>Подождите, пока он походит!</b>')
    player_avatar = await db.get_avatar(player_id)
    opponent_avatar = await db.get_avatar(opponent_id)
    async with state.proxy() as data:
        tmp_size = await db.get_game_size(player_id)
        if not all([ 1<=int(i)<=tmp_size for i in message.text.split()]):
            return await message.answer(text=f'Вы некоррентно ввели числа. Введите два числа через пробел, от 1 до {tmp_size}.')
        game = data['game']

        pole_op = await db.get_pole_op(player_id)
        pole_op = [[int(i) for i in j.split()] for j in pole_op.split(',')]
        res, pole_op = game.check_fly_list(pole_op, tmp_size, int(x)-1, int(y)-1)
        if res not in ["Попал, корабль уничтожен", "Попал"]:
            await db.set_step(player_id = player_id, queue = 'opponent')
            await db.set_step(player_id=opponent_id, queue='you')
        await bot.send_chat_action(player_id, ChatActions.TYPING)
        await asyncio.sleep(1)
        res = res + f'\nХод: {x} {y}' if "выиграли" not in res else res

        if 'выиграли' in res:
            await bot.send_photo(chat_id=player_id,
                                 photo=player_avatar)
            await message.answer(text = res,
                                 reply_markup = get_go_kb())

            await db.set_status(player_id, 'off')
            await db.set_status(opponent_id, 'off')
            await db.set_step(message.from_user.id, None)
            await state.finish()
            await bot.send_photo(chat_id=opponent_id,
                                 photo=opponent_avatar)
            await bot.send_message(chat_id = opponent_id,
                                 text=f'Вы проиграли. Игрок @{message.from_user.username} выиграл 💪\n'
                                         f'Выйдите из игры 👇, чтобы начать новую.')


        else:
            await bot.send_photo(chat_id=player_id,
                                 photo=player_avatar,
                                 caption=res)
            await bot.send_photo(chat_id=opponent_id,
                                 photo=player_avatar,
                                 caption=res)
            st_op = '0️⃣' + ''.join(['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟'][:tmp_size]) + '\n' + '\n'.join([k +
                 ''.join(['⬜️' if pole_op[i][j] in(0,1) else '💤' if pole_op[i][j] == 4 else '❎'
                    if pole_op[i][j] == 3 else '🟥' for j in range(tmp_size)])
                 for i, k in zip(range(tmp_size),[ '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟'])])

            to_op = '0️⃣' + ''.join(['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟'][:tmp_size]) + '\n' + '\n'.join([k +
                 ''.join(['⬜️' if pole_op[i][j] in(0,4) else '🟦' if pole_op[i][j] == 1 else '❎'
                    if pole_op[i][j] == 3 else '🟥' for j in range(tmp_size)])
                 for i, k in zip(range(tmp_size),[ '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟'])])

            pole_op = ','.join([' '.join([str(i) for i in j]) for j in pole_op])

            await db.set_pole(pole= pole_op, player_id= opponent_id, opponent_id=player_id)
            pole_user = await db.get_pole_my(player_id)
            pole_user = [[int(i) for i in j.split()] for j in pole_user.split(',')]

            st_user = '0️⃣' + ''.join(['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟'][:tmp_size]) + '\n' + '\n'.join([k +
                 ''.join(['⬜️' if pole_user[i][j] in(0,4) else '🟦' if pole_user[i][j] == 1 else '❎'
                    if pole_user[i][j] == 3 else '🟥' for j in range(tmp_size)])
                 for i, k in zip(range(tmp_size),[ '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟'])])

            to_user = '0️⃣' + ''.join(['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟'][:tmp_size]) + '\n' + '\n'.join([k +
                 ''.join(['⬜️' if pole_user[i][j] in(0,1) else '💤' if pole_user[i][j] == 4 else '❎'
                    if pole_user[i][j] == 3 else '🟥' for j in range(tmp_size)])
                 for i, k in zip(range(tmp_size),[ '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟'])])

            pole_user = ','.join([' '.join([str(i) for i in j]) for j in pole_user])
            await db.set_pole(pole=pole_user, player_id=player_id, opponent_id=opponent_id)



            await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
            await asyncio.sleep(1)
            await message.answer(text="Поле противника:\n"+st_op)
            await message.answer(text="Ваше поле:\n" + st_user)
            await bot.send_chat_action(opponent_id, ChatActions.TYPING)
            await asyncio.sleep(1)
            await bot.send_message(chat_id = opponent_id, text = "Поле противника:\n"+to_user)
            await bot.send_message(chat_id=opponent_id, text="Ваше поле:\n" + to_op)



@dp.message_handler(state = GameStatesGroup.play)
async def not_correct_data(message: types.Message):
    db_size = await db.get_game_size(message.from_user.id)
    await message.answer(text=f'Вы некоррентно ввели числа. Введите два числа через пробел, от 1 до {db_size}.')
