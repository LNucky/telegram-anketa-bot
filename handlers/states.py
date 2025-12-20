from aiogram.fsm.state import StatesGroup, State

class FSMState(StatesGroup):
    name = State()
    age = State()
    city = State()
    hobby = State()
    color = State()