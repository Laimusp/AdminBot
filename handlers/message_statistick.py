from sqlite3 import Connection
from datetime import datetime

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Text
from aiogram import F

router = Router()


@router.message(Text(startswith='Stat', ignore_case=True), F.from_user.id.in_({1797927303, 1145153004}))
async def get_chat_stat_handler(msg: Message, stat_connect: Connection):
    cur = stat_connect.cursor()
    date = datetime.strftime(datetime.now().date(), '%d.%m.%Y')
    chat_stat = cur.execute("SELECT count FROM info WHERE chat_id = ? AND date = ?",
                            (msg.chat.id, date)).fetchone() or (0,)
    await msg.answer(f'<b>Количество сообщений за сегодня: <u>{chat_stat[0]}</u></b>')


@router.message(F.content_type.in_({'text', 'audio', 'animation', 'sticker', 'video', 'voice', 'video_note'}))
async def update_stat_handler(msg: Message, stat_connect: Connection):
    cur = stat_connect.cursor()
    date = datetime.strftime(datetime.now().date(), '%d.%m.%Y')
    chat_stat = cur.execute("SELECT count FROM info WHERE chat_id = ? AND date = ?",
                            (msg.chat.id, date)).fetchone() or (0,)
    with stat_connect:
        if chat_stat[0] == 0:
            cur.execute("INSERT INTO info VALUES(?,?,?)", (msg.chat.id, date, 1))
        else:
            cur.execute("UPDATE info SET count = ? WHERE chat_id = ? AND date = ?",
                        (chat_stat[0] + 1, msg.chat.id, date))