from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

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
                ]
            ],
            resize_keyboard=True,
        )
