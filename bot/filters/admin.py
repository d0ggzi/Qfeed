from aiogram.filters import BaseFilter
from aiogram.types import Message
import config


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.from_user.id == int(config.admin_id)