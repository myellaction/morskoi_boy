from loader import dp
from aiogram import types
from loader import db
from keyboards.default import get_tel_num
from keyboards.inline import get_choice_ikb
from utils.states import GameStatesGroup

@dp.message_handler(text ='☑️ Регистрация')
async def registration_user(message: types.Message):
    await message.answer('Поздравляем! Вы успешно зарегистрировались.\n'
                         'Для подтверждения регистрации поделитесь своим номером телефона.',
                         reply_markup = get_tel_num())

@dp.message_handler(text='Пропустить')
@dp.message_handler(content_types = types.ContentType.CONTACT)
async def end_registration(message: types.Message):
    await message.delete()
    information = {'player_id' : message.from_user.id,
                   'full_name':message.from_user.full_name.replace(' ', '_'),
                   'username': message.from_user.username,
                   'telephone_number': message.contact.phone_number if message.contact else None}
    try:
        await db.create_user(**information)
    except:
        pass
    await GameStatesGroup.avatar.set()
    await message.answer('Чтобы начать игру, выберите аватар.',
                         reply_markup = get_choice_ikb())





