from aiogram.dispatcher.filters.state import StatesGroup, State


class GameStatesGroup(StatesGroup):
    play = State()
    avatar = State()

class PlayOne(StatesGroup):
    off = State()
    play = State()

