# Telegram Bot
=====================================

## Loyiha haqida

Bu loyiha Telegram botini yaratish uchun ishlatiladi. Bot quyidagi asosiy vazifalarni bajaradi:

### Asosiy vazifalar

* Adminlarni boshqarish: Foydalanuvchilarni admin sifatida qo'shish va o'chirish imkonini beradi. Asoschi adminni o'chirishga ruxsat berilmaydi.
* Fayllarni boshqarish: Fayllarni yuklash, saqlash va kalit so'zlar orqali ularga kirish imkonini beradi.
* Kalit so'zlar orqali fayllarni yuborish: Maxsus kalit so'zlar orqali fayllarni avtomatik ravishda yuboradi.

## Talablar

* Python 3.x
* Telethon kutubxonasi
* SQLite3

## O'rnatish

### 1. Kodlarni yuklab oling

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Python kutubxonalarini o'rnating

```bash
pip install -r requirements.txt
```

### 3. config.py faylini sozlang

`config.py` faylida quyidagi ma'lumotlarni to'ldiring:

```python
API_ID = 'YOUR_API_ID'
API_HASH = 'YOUR_API_HASH'
BOT_TOKEN = 'YOUR_BOT_TOKEN'
FOUNDER_ID = 123456789  # Asoschi adminning Telegram ID'si
FILES_FOLDER = 'files/'  # Faylni saqlash papkasi
```

## Foydalanish

### 1. Botni ishga tushiring

```bash
python main.py
```

### 2. Admin qo'shish va o'chirish

* Yangi admin qo'shish: `/addadmin <user_id>`
* Adminni o'chirish: `/kickadmin <Telegram_id>`

### 3. Fayl va kalit so'z qo'shish

`/createkeyword <kalitsoz> <faylnomi>` buyrug'i orqali fayl va kalit so'zni qo'shish mumkin.

### 4. Fayllar ro'yxatini ko'rish

`/listfiles` buyrug'i orqali barcha saqlangan fayllarni ko'rish mumkin.

### 5. Faylni o'chirish

`/delete <fayl_id>` buyrug'i orqali faylni o'chirish mumkin.

## Loyihaning tuzilishi

* `config.py`: Bot sozlamalari.
* `database.py`: Ma'lumotlar bazasi bilan ishlash funksiyalari.
* `admin.py`: Adminlarni boshqarish funksiyalari.
* `file_handler.py`: Fayllarni boshqarish funksiyalari.
* `main.py`: Botni ishga tushirish va hodisalarni boshqarish.

## Hissa qo'shish

Agar loyihaga hissa qo'shmoqchi bo'lsangiz, iltimos quyidagi qadamlarni bajaring:

1. Fork qiling.
2. Yangi branch yarating: `git checkout -b my-feature`
3. O'zgarishlarni qo'shing: `git commit -am 'Add new feature'`
4. Branchni push qiling: `git push origin my-feature`
5. Pull request yuboring.

## Litsenziya
Bu loyiha [MIT litsenziyasi](https://opensource.org/licenses/MIT) ostida tarqatiladi.