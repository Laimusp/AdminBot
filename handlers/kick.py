from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.dispatcher.filters import Text
from aiogram.exceptions import TelegramBadRequest

router = Router()


@router.message(Text(text_startswith='Kick', text_ignore_case=True))
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