from loader import dp, bot
import asyncio
from random import choice
from aiogram.types import ChatActions
from aiogram.dispatcher import FSMContext
from data.game_one import StartGame
from aiogram import types
from loader import db
from keyboards.default import get_cancel_kb, get_go_kb_one
from utils.states import PlayOne
from utils.commands import bot_avatar_choice, make_step_one



@dp.message_handler(text='🎮 Начать игру', state=PlayOne.off)
async def cmd_go(message: types.Message, state: FSMContext):
    await message.delete()
    await PlayOne.play.set()
    player_id = message.from_user.id
    await db.set_status(player_id, 'active')
    photo = await db.get_avatar(player_id)
    db_size = await db.get_game_size(player_id)
    if not db_size:
        db_size = choice(range(7,11))
        await db.set_game_size(db_size, player_id)
    async with state.proxy() as data:
        data['step']='you'
        data['bot_photo'] = await bot_avatar_choice(photo)
        data['game'] = StartGame(db_size)
        await message.answer(f"Рыба - карась, игра началась! Ваш ход.\nВведите два числа через пробел, от 1 до {db_size}.",
                         reply_markup=get_cancel_kb())



@dp.message_handler(lambda message: len(message.text.split())==2
                    and all([ i.isdigit() and 1<=int(i)<=10 for i in message.text.split()]), state = PlayOne.play)
async def computer_step(message: types.Message, state: FSMContext):
    a = message.text.split()
    player_id = message.from_user.id
    photo = await db.get_avatar(player_id)
    db_size = await db.get_game_size(player_id)
    async with state.proxy() as data:
        if not all([ 1<=int(i)<=db_size for i in message.text.split()]):
            return await message.answer(text=f'Вы некоррентно ввели числа. Введите два числа через пробел, от 1 до {db_size}.')
        game = data['game']
        if data['step'] == 'you':
            res = game.check_fly(int(a[0])-1, int(a[1])-1)

            game.user_steps.append((int(a[0])-1, int(a[1])-1))
        else:
            return await message.answer('Сейчас ход бота')



        if 'выиграл' in res:
            await PlayOne.off.set()
            await db.set_status(player_id, 'off')
            await bot.send_photo(chat_id=message.chat.id,
                                 photo=photo)
            await message.answer(text=res,
                                 reply_markup=get_go_kb_one())


        else:
            if data['step'] == 'you':
                if res not in ["Попал, корабль уничтожен", "Попал"]:
                    data['step'] ='opponent'
                await bot.send_photo(chat_id=message.chat.id,
                                 photo=photo,
                                 caption=res)
                await make_step_one(game, db_size, message, bot, data['step'])
            while data['step'] == 'opponent':
                x, y = game.computer_step()
                res = game.check_fly(x, y, 'Игрок')
                await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
                await asyncio.sleep(1)


                if 'проиграли' in res:
                    await PlayOne.off.set()
                    await db.set_status(player_id, 'off')
                    await bot.send_photo(chat_id=player_id,
                                         photo=data['bot_photo'])
                    return await message.answer(text=res,
                                         reply_markup=get_go_kb_one())

                else:
                    if res not in ["Попал, корабль уничтожен", "Попал"]:
                        data['step'] = 'you'
                    await bot.send_photo(chat_id=player_id,
                                         photo=data['bot_photo'],
                                         caption=f'Ход бота: {x + 1} {y + 1}\n{res}')
                    await make_step_one(game, db_size, message, bot, data['step'])


@dp.message_handler(state = PlayOne.play)
async def not_correct_data(message: types.Message):
    db_size = await db.get_game_size(message.from_user.id)
    await message.answer(text=f'Вы некоррентно ввели числа. Введите два числа через пробел, от 1 до {db_size}.')
