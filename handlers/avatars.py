from loader import dp, bot
from random import choice
from aiogram import types
from utils.const import avatars_list, avatars
from keyboards.inline import get_next_choice_ikb
from keyboards.default import get_go_kb, get_go_kb_one, main_menu_kb
from aiogram.dispatcher import FSMContext
from loader import db



@dp.callback_query_handler(text='choice', state = '*')
async def cb_choice(callback: types.CallbackQuery):
    await callback.message.delete()
    photo = avatars_list[0]
    await db.avatar(photo, callback.from_user.id)
    await bot.send_photo(chat_id=callback.from_user.id,
                         photo=photo,
                         caption = avatars[photo],
                         reply_markup = get_next_choice_ikb())
    await callback.answer()

@dp.callback_query_handler(text='prev', state = '*')
async def cb_choice_prev(callback: types.CallbackQuery):
    id = callback.from_user.id
    photo = await db.get_avatar(id)

    index = avatars_list.index(photo)
    if index == 0:
        index = len(avatars_list) - 1
    else:
        index-=1
    await db.avatar(avatars_list[index], id)

    await callback.message.edit_media(types.InputMedia(media=avatars_list[index],
                                                           caption=avatars[avatars_list[index]],
                                                           type='photo'),
                                           reply_markup=get_next_choice_ikb())
    await callback.answer()

@dp.callback_query_handler(text='next', state = '*')
async def cb_choice_next(callback: types.CallbackQuery):
    id = callback.from_user.id
    photo = await db.get_avatar(id)
    index = avatars_list.index(photo)
    if index == len(avatars_list) - 1:
        index = 0
    else:
        index+=1
    await db.avatar(avatars_list[index], id)
    await callback.message.edit_media(types.InputMedia(media=avatars_list[index],
                                                       caption=avatars[avatars_list[index]],
                                                       type='photo'),
                                      reply_markup=get_next_choice_ikb())
    await callback.answer()

@dp.callback_query_handler(text='set_it', state ='*')
async def cb_choice_set_it(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    photo = await db.get_avatar(callback.from_user.id)
    if not photo:
        photo = avatars_list[0]
        await db.avatar(photo, callback.from_user.id)
    st = await state.get_state()
    markup = get_go_kb if st is None else get_go_kb_one if st == 'PlayOne:off' else main_menu_kb
    if markup == main_menu_kb:
        await state.finish()
    await bot.send_photo(chat_id=callback.message.chat.id,
                             photo=photo,
                             caption=avatars[photo],
                             reply_markup=markup())
    await callback.answer()

@dp.callback_query_handler(text='random_choice', state = '*')
async def cb_random_choice(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    photo = choice(avatars_list)
    await db.avatar(photo, callback.from_user.id)
    st = await state.get_state()
    markup = get_go_kb if st is None else get_go_kb_one if st == 'PlayOne:off' else main_menu_kb
    if markup == main_menu_kb:
        await state.finish()
    await bot.send_photo(chat_id = callback.from_user.id,
                             photo = photo,
                             caption = avatars[photo],
                             reply_markup=markup())


    await callback.answer()