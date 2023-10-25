from aiogram.fsm.state import StatesGroup, State


class bot_mailing(StatesGroup):
    text = State()
    main_menu = State()