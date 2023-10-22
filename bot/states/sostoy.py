from aiogram.fsm.state import StatesGroup, State

class qfeed_state(StatesGroup):
    main_menu = State()
    add_topic = State()
    delete_topic = State()
    edit_topic = State()
    edit_topic_choice = State()
    add_channel = State()
    delete_channel = State()
    settings = State()
