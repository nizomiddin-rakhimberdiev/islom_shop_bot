from aiogram.fsm.state import State, StatesGroup

class AddCategoryState(StatesGroup):
    name = State()

class AddProductState(StatesGroup):
    name = State()
    price = State()
    description = State()
    image = State()
    category = State()


class YetkazibberishState(StatesGroup):
    phone = State()
    lokation = State()
    tolov_turi = State()