from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Text
from aiogram.exceptions import TelegramBadRequest
from aiogram import F

router = Router()


@router.message(Text(startswith='Kick', ignore_case=True), F.from_user.id.in_({1797927303, 1145153004}))
async def kick_user_handler(msg: Message, bot: Bot):
    args = msg.text.split(maxsplit=1)
    if len(args) == 1 and not msg.reply_to_message:
        await msg.answer('Вы не указали пользователя!')
        return

    if len(args) != 1:  # если написали айди чела
        try:
            await bot.kick_chat_member(msg.chat.id, int(args[1]))
        except ValueError:
            return await msg.answer('Айди должен быть цифрами!')
        except TelegramBadRequest:
            return await msg.answer('Ошибка!')
    else:
        try:
            await bot.kick_chat_member(msg.chat.id, msg.reply_to_message.from_user.id)
        except TelegramBadRequest:
            return await msg.answer('Ошибка!')

    await msg.delete()