# -*- coding: utf-8 -*-

import telebot
from telebot import types
import time
import os
import json

TOKEN = os.environ.get("BOT_TOKEN") or "7628596509:AAGFcAqqTWbSKMdyx2PFAwiCTmi6HFqrH-M"
bot = telebot.TeleBot(TOKEN)

# ID вашей группы для отправки резерваций
GROUP_ID = "-1002821346634"

# Файл для хранения резерваций
reservations_file = "reservations.json"

# Память для незавершённых резерваций
pending_reservations = {}

def load_reservations():
    try:
        with open(reservations_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_reservations(data):
    with open(reservations_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("📄 Скачать прайс-листы"))
    markup.add(types.KeyboardButton("📷 Галерея Toza Marković"))
    markup.add(types.KeyboardButton("🌐 Перейти на сайт"))
    #markup.add(types.KeyboardButton("🎉 Актуальные акции"))
    markup.add(types.KeyboardButton("📞 Контакты"))
    markup.add(types.KeyboardButton("📝 Резервация объекта"))
    return markup

def cancel_button():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("❌ Отмена"))
    return markup

@bot.message_handler(commands=["start", "menu"])
def start(message):
    pending_reservations.pop(message.chat.id, None)  # если юзер вернулся в меню, отменяем резервацию
    bot.send_message(
        message.chat.id,
        "Привет! 👋\nВыбери действие в меню ниже:",
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda m: True)
def menu_handler(message):
    if message.text == "📄 Скачать прайс-листы":
        pending_reservations.pop(message.chat.id, None)
        bot.send_message(message.chat.id, "📩 Отправка прайс-листов…", reply_markup=main_menu())
        files = ["ПРАЙС_СКЛАДЫ_09_03_2026_МИР_КЕРАМИКИ.xlsx", "ПРАЙС_КРОВЛЯ_12.03.26_МИР_КЕРАМИКИ.xlsx"]
        for filename in files:
            try:
                with open(filename, "rb") as f:
                    bot.send_document(message.chat.id, f)
            except FileNotFoundError:
                bot.send_message(message.chat.id, f"❌ Файл {filename} не найден.")
        bot.send_message(message.chat.id, "✅ Прайс-листы отправлены", reply_markup=main_menu())

    elif message.text == "📷 Галерея Toza Marković":
        pending_reservations.pop(message.chat.id, None)
        bot.send_message(message.chat.id, "📷 Галерея: https://toza.rs/prodavnica/crep/", reply_markup=main_menu())

    elif message.text == "🌐 Перейти на сайт":
        pending_reservations.pop(message.chat.id, None)
        bot.send_message(message.chat.id, "🌐 Сайт: https://mirkeramiki.org", reply_markup=main_menu())

    elif message.text == "🎉 Актуальные акции":
        pending_reservations.pop(message.chat.id, None)
        try:
            with open("promo.jpg", "rb") as photo:
                bot.send_photo(message.chat.id, photo, reply_markup=main_menu())
        except FileNotFoundError:
            bot.send_message(message.chat.id, "❌ promo.jpg не найден", reply_markup=main_menu())

    elif message.text == "📞 Контакты":
        pending_reservations.pop(message.chat.id, None)
        contacts_text = (
            "📍 *Наши контакты:*\n\n"
            "🏢 *Офис*\n"
            "📞 +380503909383 (Олег)\n"
            "📞 +380979560464 (Евгений)\n"
            "📍 [г. Одесса, ул. Левитана 62](https://maps.app.goo.gl/9ou4bG5fH8zHbig99)\n\n"
            "🏢 *Склад №1*\n"
            "📞 +380950411490 (Андрей)\n"
            "📍 [г. Одесса, Киевское шоссе 2](https://maps.app.goo.gl/73Y6FzuPiuTsEMP98)\n\n"
            "🏢 *Склад №2*\n"
            "📞 +380505190818 (Вадим)\n"
            "📍 [с. Нерубайское, Пастера 1](https://maps.app.goo.gl/zwmnNe8YdUPbrmWw8)"
        )
        bot.send_message(message.chat.id, contacts_text, parse_mode="Markdown", disable_web_page_preview=True, reply_markup=main_menu())

    elif message.text == "📝 Резервация объекта":
        pending_reservations[message.chat.id] = {}
        msg = bot.send_message(message.chat.id, "Введите адрес объекта (или нажмите Отмена):", reply_markup=cancel_button())
        bot.register_next_step_handler(msg, process_address)

    elif message.text == "❌ Отмена":
        pending_reservations.pop(message.chat.id, None)
        bot.send_message(message.chat.id, "❌ Резервация отменена", reply_markup=main_menu())

    else:
        bot.send_message(message.chat.id, "Неизвестная команда. Выберите из меню.", reply_markup=main_menu())


# ====== Шаги резервации ======

def process_address(message):
    if message.text == "❌ Отмена":
        pending_reservations.pop(message.chat.id, None)
        bot.send_message(message.chat.id, "❌ Резервация отменена", reply_markup=main_menu())
        return

    address = message.text.strip()
    reservations = load_reservations()
    if address in reservations:
        bot.send_message(message.chat.id, "❌ Этот объект уже зарезервирован!", reply_markup=main_menu())
        pending_reservations.pop(message.chat.id, None)
        return

    pending_reservations[message.chat.id]["address"] = address
    msg = bot.send_message(message.chat.id, "Введите вид материалов и их количество (или Отмена):", reply_markup=cancel_button())
    bot.register_next_step_handler(msg, process_volume)

def process_volume(message):
    if message.text == "❌ Отмена":
        pending_reservations.pop(message.chat.id, None)
        bot.send_message(message.chat.id, "❌ Резервация отменена", reply_markup=main_menu())
        return

    pending_reservations[message.chat.id]["volume"] = message.text.strip()
    msg = bot.send_message(message.chat.id, "Введите последние 4 цифры номера заказчика (или Отмена):", reply_markup=cancel_button())
    bot.register_next_step_handler(msg, process_contact)

def process_contact(message):
    if message.text == "❌ Отмена":
        pending_reservations.pop(message.chat.id, None)
        bot.send_message(message.chat.id, "❌ Резервация отменена", reply_markup=main_menu())
        return

    contact = message.text.strip()
    if len(contact) != 4 or not contact.isdigit():
        msg = bot.send_message(message.chat.id, "Неверный формат. Введите 4 цифры:", reply_markup=cancel_button())
        bot.register_next_step_handler(msg, process_contact)
        return

    data = pending_reservations.pop(message.chat.id, {})
    if not data:
        bot.send_message(message.chat.id, "⚠️ Ошибка. Попробуйте снова.", reply_markup=main_menu())
        return

    data["contact"] = contact

    reservations = load_reservations()
    reservations[data["address"]] = {
        "user_id": message.from_user.id,
        "username": message.from_user.username or message.from_user.first_name,
        "volume": data["volume"],
        "contact": data["contact"]
    }
    save_reservations(reservations)

    username_display = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name

    text = (
        f"📌 Новая резервация:\n\n"
        f"👤 Ответственный: {username_display}\n"
        f"🏠 Адрес объекта: {data['address']}\n"
        f"📦 Материал и количество: {data['volume']}\n"
        f"📞 Контакт заказчика (последние 4 цифры): {data['contact']}"
    )
    bot.send_message(GROUP_ID, text)
    bot.send_message(message.chat.id, "✅ Резервация успешно сохранена!", reply_markup=main_menu())


# ====== Запуск ======

print("Бот запущен...")

if __name__ == "__main__":
    while True:
        try:
            bot.infinity_polling(timeout=60, long_polling_timeout=90)
        except Exception as e:
            print(f"Ошибка polling: {e}")
            time.sleep(5)




