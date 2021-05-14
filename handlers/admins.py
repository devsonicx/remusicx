from asyncio import QueueEmpty
from datetime import datetime
from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import os
import aiohttp
from random import randint
import aiofiles
from callsmusic import callsmusic, queues

from helpers.filters import command, other_filters
from helpers.decorators import errors, authorized_users_only


@Client.on_message(command("تعليق") & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
    if callsmusic.pause(message.chat.id):
        await message.reply_text(" ⏸ تم إيقافه مؤقتاً!")
    else:
        await message.reply_text("لايوجد شيء يعمل لكي اقوم بايقافه! ☹️")

@Client.on_message(command("اوامر الصوت") & other_filters)
@errors
@authorized_users_only
async def help(_, message: Message):
    await message.reply_text(
        f"""أنا بوت ✦ ABAZA🎶 
وأسمح لك بتشغيل الموسيقى في المكالمات الصوتية لمجموعتك. 🎵
الأوامر التي أدعمها حاليًا هي:
تشغيل - 🎼 قم بالرد على ملف الموسيقى او على رابط يوتيوب لتشغيله
تعليق - ▶️ إيقاف البث الصوتي مؤقتاً
استئناف - ⏸ اعادة تشغيل الموسيقى المعلقة
تخطي - ↪️ تخطي الموصيقى المشغلة حالياً
كتم - 🔇 كتم صوت البوت
الغاء الكتم - 🔊 الغاء كتم صوت البوت
ايقاف - 🗑🛑 ايقاف تشغيل الموسيقى ومغادرة المكالمة
السرعة - 📊 لحساب سرعة استجابة البوت
ديزر - 🎶 للبحث عن اغنية وتحميلها من موقع deezer
        """,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "مطور البوت 👨🏻‍💻 ", url="https://t.me/IlIIl_I"
                    ),
                    InlineKeyboardButton(
                        "قناة البوت ♥", url="https://t.me/jjxxh"
                    )
                ]
            ]
        )
    )
        
ARQ = "https://thearq.tech/"
# fetch url for deezer download
async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            try:
                data = await resp.json()
            except:
                data = await resp.text()
    return data
    
async def download_song(url):
    song_name = f"{randint(6969, 6999)}.mp3"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(song_name, mode="wb")
                await f.write(await resp.read())
                await f.close()
    return song_name

# deezer download by william butcher bot
@Client.on_message(command("ديزر") & other_filters)
@errors
@authorized_users_only
async def deezer(_, message: Message):
    if len(message.command) < 2:
        await message.reply_text("لم تقم بوضع اسم الاغنية بعد كلمة ديزر 🧐")
        return
    text = message.text.split(None, 1)[1]
    query = text.replace(" ", "%20")
    dsaied = await message.reply_text("يتم البحث... 🔎")
    try:
        r = await fetch(f"{ARQ}deezer?query={query}&count=1")
        title = r[0]["title"]
        url = r[0]["url"]
        artist = r[0]["artist"]
    except Exception as e:
        await dsaied.edit_text(str(e))
        return
    await dsaied.edit_text("يتم التحميل... 🎶")
    song = await download_song(url)
    await dsaied.edit_text("يتم الرفع... 🎶")
    await message.reply_audio(audio=song, title=title, performer=artist)
    os.remove(song)
    await dsaied.delete()
    
@Client.on_message(command("السرعة") & other_filters)
@errors
@authorized_users_only
async def ping(_, message: Message):
    start = datetime.now()
    res = await message.reply_text('`يتم حساب السرعة!`')
    end = datetime.now()
    latency = (end - start).microseconds / 1000
    await res.edit_text(f"**البوت يعمل!**\n📊 السرعة : `{latency} ms`")


@Client.on_message(command("استئناف") & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    if callsmusic.resume(message.chat.id):
        await message.reply_text(" ▶️ تم اعادة تشغيله... ")
    else:
        await message.reply_text("لم يتم ايقاف اي شيء لكي اعيد تشغيله! 🤷‍♂️")


@Client.on_message(command("ايقاف") & other_filters)
@errors
@authorized_users_only
async def stop(_, message: Message):
    if message.chat.id not in callsmusic.active_chats:
        await message.reply_text("لا يتم تشغيل شيء ☹️")
    else:
        try:
            queues.clear(message.chat.id)
        except QueueEmpty:
            pass

        await callsmusic.stop(message.chat.id)
        await message.reply_text("🗑 تم مسح قائمه الانتظار ومغادرة المكالمة... 🏃")


@Client.on_message(command("تخطي") & other_filters)
@errors
@authorized_users_only
async def skip(_, message: Message):
    if message.chat.id not in callsmusic.active_chats:
        await message.reply_text("لا يتم تشغيل شيء ☹️")
    else:
        queues.task_done(message.chat.id)

        if queues.is_empty(message.chat.id):
            await callsmusic.stop(message.chat.id)
        else:
            await callsmusic.set_stream(
                message.chat.id, queues.get(message.chat.id)["file"]
            )

        await message.reply_text("تم التخطي! ↪")


@Client.on_message(command("كتم") & other_filters)
@errors
@authorized_users_only
async def mute(_, message: Message):
    result = callsmusic.mute(message.chat.id)

    if result == 0:
        await message.reply_text("🔇 تم كتم الصوت ")
    elif result == 1:
        await message.reply_text("🤐 تم كتم الصوت بالفعل!")
    elif result == 2:
        await message.reply_text("🎙❎ ليس داخل المكالمة الصوتية!")


@Client.on_message(command("الغاء الكتم") & other_filters)
@errors
@authorized_users_only
async def unmute(_, message: Message):
    result = callsmusic.unmute(message.chat.id)

    if result == 0:
        await message.reply_text("🔊 تم الغاء الكتم بنجاح!")
    elif result == 1:
        await message.reply_text("😆 تم  الغاء الكتم بالتاكيد!")
    elif result == 2:
        await message.reply_text("🎙❎ ليس داخل المكالمة الصوتية")
