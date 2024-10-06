from telethon import events
import database
import config

async def add_admin_handler(event):
    if event.is_group:
        await event.reply('Bu buyruq shaxsiy xabarda ishlatilishi kerak.')
        return

    # Faqat asosiy admin boshqa foydalanuvchilarni admin sifatida qo'sha oladi
    if not is_admin(event.sender_id):
        await event.reply('Sizda bu buyruqdan foydalanish huquqi yo\'q.')
        return

    parts = event.raw_text.split(maxsplit=1)
    if len(parts) != 2:
        await event.reply('Foydalanish: `/addadmin` <user_id>')
        return
    user_id = int(parts[1])

    if is_admin(user_id):
        await event.reply(f'Foydalanuvchi allaqachon admin: {user_id}.')
    else:
        # Telegram foydalanuvchi nomini olish
        user = await event.client.get_entity(user_id)
        telegram_username = user.username if user.username else "Oddiy Admin"
        database.add_admin(user_id, telegram_username)
        await event.reply(f'Admin sifatida qo\'shildi: {user_id}.')

async def delete_admin_handler(event):
    if event.is_group:
        await event.reply('Bu buyruq shaxsiy xabarda ishlatilishi kerak.')
        return

    if not is_admin(event.sender_id):
        await event.reply('Sizda bu buyruqdan foydalanish huquqi yo\'q.')
        return

    parts = event.raw_text.split(maxsplit=1)
    if len(parts) != 2:
        await event.reply('Foydalanish: `/kickadmin` <Telegram_id>')
        return
    user_id = int(parts[1])
    
    # Asoschi adminni o'chirishga ruxsat bermaymiz
    if user_id == config.FOUNDER_ID:
        await event.reply('Asoschi adminni o\'chirishga ruxsat berilmaydi.\n\n**Damingni ol 😏**')
        return

    if database.delete_admin(user_id):
        await event.reply(f'Admin o\'chirildi: **{user_id}**.')
    else:
        await event.reply(f'Admin topilmadi: **{user_id}**.')

async def admin_list_handler(event):
    # Faqat adminlar ro'yxatni ko'rishi mumkin
    if not is_admin(event.sender_id):
        await event.reply('Sizda bu buyruqdan foydalanish huquqi yo\'q.')
        return

    admins = database.get_all_admins()
    if admins:
        response = "Adminlar ro'yxati:\n"
        for admin in admins:
            response += f"ID: {admin[0]} | Telegram ID: `{admin[1]}` | Status: {admin[2]}\n"
        await event.reply(response)
    else:
        await event.reply('Hech qanday admin topilmadi.')

def is_admin(user_id):
    return database.is_admin(user_id)

def ensure_founder_exists():
    # Asoschini ma'lumotlar bazasida mavjudligini tekshirish
    if not database.is_admin(config.FOUNDER_ID):
        # Asoschini qo'shish
        database.add_admin(config.FOUNDER_ID, "Asoschi")