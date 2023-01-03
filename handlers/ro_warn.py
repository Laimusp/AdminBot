import time
from sqlite3 import Connection

from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.types.chat_permissions import ChatPermissions
from aiogram.filters import Text
from aiogram import F

router = Router()


@router.message(Text(startswith='RO', ignore_case=True), F.from_user.id.in_({1797927303, 1145153004}))
async def ro_warn_handler(msg: Message, bot: Bot, ro_connect: Connection):
    if reply := msg.reply_to_message:
        cur = ro_connect.cursor()
        user_id = reply.from_user.id
        ro_count = cur.execute(f"SELECT ro FROM users WHERE user_id = {user_id}").fetchone() or (0,)

        with ro_connect:
            if ro_count[0] == 0:
                cur.execute("INSERT INTO users(user_id, ro) VALUES(?, ?)", (user_id, 1))
            elif ro_count[0] + 1 == 3:
                await bot.ban_chat_member(msg.chat.id, user_id)
                cur.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
                return
            else:
                cur.execute("UPDATE users SET ro = ? WHERE user_id = ?", (ro_count[0] + 1, user_id))

            await bot.restrict_chat_member(
                msg.chat.id,
                user_id,
                ChatPermissions(can_send_message=False),
                until_date=int(time.time() + 30 * 60)
            )