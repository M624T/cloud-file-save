from telethon import events
import database
import config
from admin import is_admin

import PIL
import os


# Fayl kalit so'zini yaratish uchun handler
async def create_keyword_handler(event):
    # Tekshiramiz agar foydalanuvchi admin ekan
    if is_admin(event.sender_id):
        # Buyruqni ajratamiz
        parts = event.raw_text.split(maxsplit=2)

        # Buyruq formati to'g'riligini tekshiramiz
        if len(parts) == 3:
            # Kalit so'z va fayl nomini o'qib olamiz
            keyword = parts[1]  # Kalit so'z
            name = parts[2]  # Fayl nomi

            # Adminni faylni yuborishga taklif qilamiz
            await event.reply("Faylni yuboring.\nFayl hajmi 50Mb dan oshmaslikni tavsiya qilamiz.", reply_to=event.id)


            # Admin yuborgan faylni kutamiz
            @event.client.on(events.NewMessage(from_users=event.sender_id, func=lambda e: e.file))
            async def handler(response):
                    # Faylni yuklab olamiz
                await event.reply(f"Kuting yuklanmoqda...")
                await event.client.send_message(event.sender_id, "⌛")
                file_path = await event.client.download_media(response.message, config.FILES_FOLDER)

                # Fayl va kalit so'zni ma'lumotlar bazasiga saqlaymiz
                database.save_file(name, keyword, file_path, event.sender_id)
                await event.reply(f"Muvaffaqiyatli saqlandi: **{name}** \nKalit so'z `{keyword}`")

        else:
            # Buyruq noto'g'ri yozilganligi haqida xabar beramiz
            await event.reply("Buyruq noto'g'ri yozildi. Foydalanish: `/createkeyword` <kalitsoz> <faylnomi>")
    else:
        # Foydalanuvchi admin emasligi haqida xabar beramiz
        await event.reply("Sizda bu buyruqdan foydalanish huquqi yo'q.")


# Maxsus kalit so'zni tekshirish va faylni jo'natish
async def handle_keyword(event, keyword):
    try:
        # Kelgan xabarni kichik harfga o'zgartirish va bo'shliqlar bo'yicha ajratish
        incoming_message_words = event.raw_text.lower().split()

        # Kalit so'zni to'liq so'z sifatida tekshirish
        if keyword in incoming_message_words:
            # Fayl ma'lumotlarini olish
            file_data = database.get_file_by_keyword(keyword)

            # Fayl topilganligini tekshirish
            if file_data:
                file_name, file_path = file_data
                await event.reply(f"Faylni yuklab olishingiz mumkin: **{file_name}**")
                await event.client.send_file(event.sender_id, file_path)
            else:
                await event.reply("Kalit so'z bo'yicha fayl topilmadi.")
        else:
            await event.reply("Kalit so'z topilmadi yoki noto'g'ri kiritildi.")
    except Exception as e:
        await event.reply(f"Xatolik yuz berdi: {str(e)}")


# Fayllar ro'yxatini ko'rish
async def list_files_handler(event):
    # Adminligini tekshirish
    if is_admin(event.sender_id):
        # Barcha fayllarni olish
        files = database.get_all_files()

        # Fayllar topilganligi haqida xabar berish
        if files:
            response = "Fayllar ro'yxati:\n"
            for file in files:
                response += f"ID: {file[0]} | Nomi: **{file[1]}** | Kalit so'z: `{file[2]}` |\n"  # Yo'l: {file[3]}\n"
            await event.reply(response)
        else:
            # Hech qanday fayl topilmaganligi haqida xabar berish
            await event.reply("Hech qanday fayl topilmadi.")
    else:
        # Admin emasligi haqida xabar berish
        await event.reply("Sizda bu buyruqdan foydalanish huquqi yo'q.")


# Faylni o'chirish
async def delete_file_handler(event):
    # Adminligini tekshirish
    if is_admin(event.sender_id):
        # Buyruqni ajratish
        parts = event.raw_text.split()

        # Foydalanish formati tekshiriladi
        if len(parts) == 2:
            # Fayl ID sini olish
            file_id = int(parts[1])

            # Fayl ma'lumotlarini olish
            file_data = database.get_file_by_id(file_id)

            # Fayl topilganligi haqida xabar berish
            if file_data:
                # Fayl yo'lini olish
                file_path = file_data[3]

                # Faylni ma'lumotlar bazasidan o'chirish
                if database.delete_file(file_id):
                    try:
                        # Faylni diskdan o'chirish
                        os.remove(file_path)
                        await event.reply(
                            f"ID: {file_id} bo'lgan fayl muvaffaqiyatli o'chirildi."
                        )
                    except FileNotFoundError:
                        # Fayl diskdan topilmaganligi haqida xabar berish
                        await event.reply(
                            "Fayl ma'lumotlar bazasidan o'chirildi, lekin diskdan topilmadi."
                        )
                else:
                    # Fayl o'chirishda xato yuz berganligi haqida xabar berish
                    await event.reply("Fayl topilmadi yoki o'chirishda xato yuz berdi.")
            else:
                # Fayl topilmaganligi haqida xabar berish
                await event.reply("Fayl topilmadi.")
        else:
            # Buyruq noto'g'ri yozilganligi haqida xabar berish
            await event.reply(
                "Buyruq noto'g'ri yozildi . Foydalanish: `/delete` <fayl_id>"
            )
    else:
        # Admin emasligi haqida xabar berish
        await event.reply("Sizda bu buyruqdan foydalanish huquqi yo'q.")
