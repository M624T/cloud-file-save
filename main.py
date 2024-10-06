from telethon import TelegramClient, events
import config
import admin
import file_handler
import database


def main():
    database.create_admin_table()
    database.create_file_table()

    # Asoschini qo'shish
    admin.ensure_founder_exists()

    client = TelegramClient("bot", config.API_ID, config.API_HASH).start(
        bot_token=config.BOT_TOKEN
    )

    client.on(events.NewMessage(pattern="/addadmin"))(admin.add_admin_handler)
    client.on(events.NewMessage(pattern="/createkeyword"))(
        file_handler.create_keyword_handler
    )

    # Maxsus kalit so'zni tekshirish
    @client.on(events.NewMessage)
    async def keyword_handler(event):
        # Agar xabar / belgisi bilan boshlangan bo'lsa, funksiyani yakunlash
        if event.raw_text.startswith('/'):
            return
        
        incoming_message_words = (
            event.raw_text.lower().split()
        )  # Xabarni kichik harflarga o'zgartirib, bo'shliqlar bo'yicha ajratish
        keywords = [file[2] for file in database.get_all_files()]

        # Kalit so'z topilganligini aniqlash uchun flag
        keyword_found = False

        for keyword in keywords:
            if (
                keyword in incoming_message_words
            ):  # Kalit so'zni to'liq so'z sifatida tekshirish
                await file_handler.handle_keyword(event, keyword)
                keyword_found = True
                break

        # Agar kalit so'z topilmasa, foydalanuvchiga xabar yuborish
        if not keyword_found:
            await event.reply("Bunday kalit so'z mavjud emas.")

    client.on(events.NewMessage(pattern="/kickadmin"))(admin.delete_admin_handler)
    client.on(events.NewMessage(pattern="/listfiles"))(file_handler.list_files_handler)
    client.on(events.NewMessage(pattern="/delete"))(file_handler.delete_file_handler)
    client.on(events.NewMessage(pattern="/adminlist"))(admin.admin_list_handler)

    client.run_until_disconnected()


if __name__ == "__main__":
    main()
