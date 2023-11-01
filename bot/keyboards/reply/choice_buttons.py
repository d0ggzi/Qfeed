from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonRequestChat

menu = ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Редактировать тему"),
                ],
                [
                    KeyboardButton(text="Добавить тему"),
                    KeyboardButton(text="Удалить тему"),
                ], 
                [
                    KeyboardButton(text="Настройки"),
                ],
                [
                    KeyboardButton(text='Вернуться в меню')
                ]
            ],
            resize_keyboard=True,
        )

edit_theme_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Добавить канал'), #, request_chat=KeyboardButtonRequestChat(request_id=1, chat_is_channel=True)
            KeyboardButton(text='Удалить канал')
        ],
        [
            KeyboardButton(text='Вернуться в меню')
        ]
    ],
    resize_keyboard=True,
)

go_to_main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Вернуться в меню')]
    ],
    resize_keyboard=True
)