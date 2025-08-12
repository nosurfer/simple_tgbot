from aiogram.fsm.state import State, StatesGroup

class OwnMessage(StatesGroup):
    message = State()