from aiogram.fsm.state import StatesGroup, State

class qfeed_state(StatesGroup):
    main_menu = State()
    add_theme = State()
    delete_theme = State()
    edit_theme = State()
    settings = State()

