from loader import dp
from aiogram.dispatcher import FSMContext
from aiogram import types
from keyboards.inline import get_choice_ikb, get_size_ikb
from utils.const import *
from utils.states import PlayOne, GameStatesGroup
from loader import db
from keyboards.default import get_registration, get_go_kb, get_go_kb_one, main_menu_kb


# 🎮🗣❓♻️✅👤❌📐

@dp.message_handler(commands=['start'], state = '*')
async def cmd_start(message: types.Message, state: FSMContext):
    await message.delete()
    await state.finish()
    user_id = message.from_user.id
    await db.set_status(user_id, 'off')
    await db.set_game_size(0, user_id)
    await db.set_opponent(user_id, None)
    await db.set_step(user_id, None)
    avatar = await db.get_avatar(user_id)
    if not (await db.get_user(user_id)):
        await message.answer('Добро пожаловать в бот. Чтобы начать игру, нажмите <b>"Регистрация"</b>.',
                             reply_markup = get_registration())
    elif not avatar:
        await GameStatesGroup.avatar.set()
        await message.answer(text='Добро пожаловать в бот. Чтобы начать игру, выберите аватар.',
                         reply_markup = get_choice_ikb())
    else:
        await message.answer(text='Добро пожаловать в бот. Ваш аватар.')
        await message.answer_photo(photo=avatar,
                             caption=avatars[avatar],
                             reply_markup=main_menu_kb())


@dp.message_handler(text='❓ Справка', state = [None, PlayOne.off])
async def cmd_help(message: types.Message):
    await message.delete()
    await message.answer(text=text, parse_mode ='HTML')

@dp.message_handler(text='❌ Выйти из игры', state='*')
async def cmd_cancel(message: types.Message, state: FSMContext):
    await message.delete()
    st = await state.get_state()
    if st == 'GameStatesGroup:play':
        markup = get_go_kb
        await state.finish()
    else:
        markup = get_go_kb_one
        await PlayOne.off.set()
    await message.answer(text='Вы вышли из игры.',
                         reply_markup = markup())
    await db.set_status(message.from_user.id, 'off')
    await db.set_step(message.from_user.id, None)



@dp.message_handler(text='👤 Изменить аватар', state = [None, PlayOne.off])
async def cmd_start(message: types.Message):
    await message.delete()
    await message.answer(text='Меню выбора аватара',
                         reply_markup = get_choice_ikb())

@dp.message_handler(text='📐 Изменить размер поля', state = [None, PlayOne.off])
async def cmd_start(message: types.Message):
    await message.delete()
    await message.answer(text='Выберите размер игрового поля',
                         reply_markup = get_size_ikb())

@dp.message_handler(text='🏠 Главное меню', state = [None, PlayOne.off])
async def cmd_start(message: types.Message, state: FSMContext):
    await message.delete()
    await state.finish()
    st = await state.get_state()
    if st is None:
        await db.set_opponent(message.from_user.id)
    await message.answer(text='Выберите тип игры 👇',
                         reply_markup = main_menu_kb())

@dp.message_handler(text='⛴ Одиночная игра')
async def cmd_start(message: types.Message):
    await message.delete()
    await PlayOne.off.set()
    await message.answer(text='Меню одиночной игры',
                         reply_markup = get_go_kb_one())

@dp.message_handler(text='🚢 Мультиплеер')
async def cmd_start(message: types.Message):
    await message.delete()
    await message.answer(text='Меню мультиплеера',
                         reply_markup = get_go_kb())