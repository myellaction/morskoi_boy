from utils.const import avatars_list
from random import choice
import asyncio
from aiogram.types import ChatActions
from keyboards.default import get_cancel_kb

async def bot_avatar_choice(photo):
    bot_photo = choice (avatars_list)
    while bot_photo == photo:
        bot_photo = choice(avatars_list)
    return bot_photo

async def make_step_one(game, db_size, message,bot,step):

    computer_pole = list(game.computer.get_pole())
    user_pole = list(game.user.get_pole())
    st_c = '0️⃣'+ ''.join(['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟'][:db_size]) + '\n' + '\n'.join([k +
                    ''.join(['⬜️' if (nj, n) not in game.user_steps else '💤' if computer_pole[nj][n] == 0 else '❎'
                    if computer_pole[nj][n] == 3 else '🟥'
                    for n, i in enumerate(j)]) for (nj, j), k in zip(enumerate(computer_pole),
                    ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟'])])
    st_u = '0️⃣'+ ''.join(['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟'][:db_size]) + '\n' + '\n'.join([k +
                    ''.join(['⬜️' if i == 0 else '🟦' if i == 1 else '❎' if i ==3 else '🟥' for i in j])
                    for j, k in zip(user_pole, ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣','🔟'])])
    await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
    await asyncio.sleep(1)
    await message.answer(text=f'Поле бота:\n{st_c}')
    await asyncio.sleep(1)
    step = 'Ваш ход!' if step =='you' else 'Ход бота!'
    await message.answer(text=f'Ваше поле:\n{st_u}\n<b>{step}</b>', reply_markup=get_cancel_kb())

