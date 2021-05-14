from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from helpers.filters import other_filters2


@Client.on_message(other_filters2)
async def start(_, message: Message):
    await message.reply_text(
        f"""أنا بوت  ريميوزك🎶 
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
                        "مطور البوت 👨🏻‍💻 ", url="https://t.me/U660P"
                    ),
                    InlineKeyboardButton(
                        "قناة البوت ♥", url="https://t.me/UU_FUCK"
                    )
                ]
            ]
        )
    )
