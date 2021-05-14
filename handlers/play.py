from os import path

from pyrogram import Client
from pyrogram.types import Message, Voice

from callsmusic import callsmusic, queues

import converter
from downloaders import youtube

from config import DURATION_LIMIT
from helpers.errors import DurationLimitError
from helpers.filters import command, other_filters
from helpers.decorators import errors


@Client.on_message(command("تشغيل") & other_filters)
@errors
async def play(_, message: Message):
    audio = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None

    res = await message.reply_text("🚀 يتم المعالجة...")

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"غير مسموح بمقاطع الموسيقى التي تزيد مدتها عن {DURATION_LIMIT} دقيقة ، الموسيقى المقدم مدته {audio.duration / 60} دقيقة"
            )

        file_name = audio.file_unique_id + "." + (
            audio.file_name.split(
                ".")[-1] if not isinstance(audio, Voice) else "ogg"
        )
        file = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name)) else file_name
        )
    else:
        messages = [message]
        text = ""
        offset = None
        length = None

        if message.reply_to_message:
            messages.append(message.reply_to_message)

        for _message in messages:
            if offset:
                break

            if _message.entities:
                for entity in _message.entities:
                    if entity.type == "url":
                        text = _message.text or _message.caption
                        offset, length = entity.offset, entity.length
                        break

        if offset in (None,):
            await res.edit_text("انت لم تعطني أي شيء لتشغيله 👀😆")
            return

        url = text[offset:offset + length]
        file = await converter.convert(youtube.download(url))

    if message.chat.id in callsmusic.active_chats:
        position = await queues.put(message.chat.id, file=file)
        await res.edit_text(f"✅ تم اضافته الى قائمة الانتظار {position} 🎧")
    else:
        await res.edit_text("🎶 تم تشغيله...")
        await callsmusic.set_stream(message.chat.id, file)
