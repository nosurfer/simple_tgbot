from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    name = State()
    direction = State()
    about = State()
    confirm = State()

    done = State()