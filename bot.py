# -*- coding: utf-8 -*-

import telebot
from telebot import types
import time
import os
import json

TOKEN = os.environ.get("BOT_TOKEN") or "7628596509:AAH-GgXWnMJlUUs9mMPr9PRiy-gRr6h3AYY"
bot = telebot.TeleBot(TOKEN)

# ID вашей группы для отправки резерваций
GROUP_ID = "1015977236"  # замените на свой id группы

# Файл для хранения резерваций
reservations_file = "reservations.json"

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
    markup.add(types.KeyboardButton("🎉 Актуальные акции"))
    markup.add(types.KeyboardButton("📞 Контакты"))
    markup.add(types.KeyboardButton("📝 Резервация объекта"))  # новая кнопка
    return markup

@bot.message_handler(commands=["start", "menu"])
def start(message):
    bot.send_message(
        message.chat.id,
        "Привет! 👋\nВыбери действие в меню ниже:",
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda m: True)
def menu_handler(message):
    if message.text == "📄 Скачать прайс-листы":
        bot.send_message(message.chat.id, "📩 Отправка прайс-листов… Это может занять несколько секунд.", reply_markup=main_menu())
        files = ["Прайс_общестрой.xlsx", "Прайс_кровельный.xls"]
        for filename in files:
            try:
                with open(filename, "rb") as f:
                    bot.send_document(message.chat.id, f)
            except FileNotFoundError:
                bot.send_message(message.chat.id, f"❌ Файл {filename} не найден. Добавьте его рядом с bot.py", reply_markup=main_menu())
        bot.send_message(message.chat.id, "Прайс-листы отправлены ✅", reply_markup=main_menu())

    elif message.text == "📷 Галерея Toza Marković":
        bot.send_message(message.chat.id, "📷 Галерея Toza Marković здесь:\nhttps://toza.rs/prodavnica/crep/", reply_markup=main_menu())

    elif message.text == "🌐 Перейти на сайт":
        bot.send_message(message.chat.id, "🌐 Мой сайт:\nhttps://mirkeramiki.org", reply_markup=main_menu())

    elif message.text == "🎉 Актуальные акции":
        try:
            with open("promo.jpg", "rb") as photo:
                bot.send_photo(message.chat.id, photo, reply_markup=main_menu())
        except FileNotFoundError:
            bot.send_message(message.chat.id, "❌ Картинка promo.jpg не найдена", reply_markup=main_menu())

    elif message.text == "📞 Контакты":
        contacts_text = (
            "📍 *Наши контакты:*\n\n"
            "🏢 *Офис*\n"
            "📞 +380503909383 (Олег Баранов - общестрой)\n"
            "📞 +380979560464 (Евгений Рогачко - кровля)\n"
            "📍 [г. Одесса, ул. Левитана 62](https://maps.app.goo.gl/R4ULrDniGVGfqpjm6)\n\n"
            "🏢 *Склад №1*\n"
            "📞 +380950411490 (кладовщик Андрей)\n"
            "📍 [г. Одесса, Киевское шоссе 2](https://maps.app.goo.gl/RkA5sAu6pZ7nbjHe6)\n\n"
            "🏢 *Склад №2*\n"
            "📞 +380505190818 (кладовщик Вадим)\n"
            "📍 [с. Нерубайское, Пастера 1](https://maps.app.goo.gl/SHzNKh9Kyid4SzdR8)"
        )
        bot.send_message(
            message.chat.id,
            contacts_text,
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=main_menu()
        )

    elif message.text == "📝 Резервация объекта":
        msg = bot.send_message(message.chat.id, "Введите адрес объекта:")
        bot.register_next_step_handler(msg, process_address)

    else:
        bot.send_message(message.chat.id, "Неизвестная команда. Пожалуйста, выберите действие из меню.", reply_markup=main_menu())


# ====== Функции резервации ======

def process_address(message):
    address = message.text.strip()
    reservations = load_reservations()
    if address in reservations:
        bot.send_message(message.chat.id, "❌ Этот объект уже зарезервирован!")
        return
    user_data = {"address": address}
    msg = bot.send_message(message.chat.id, "Введите вид материалов и их количество:")
    bot.register_next_step_handler(msg, process_volume, user_data)

def process_volume(message, user_data):
    user_data["volume"] = message.text.strip()
    msg = bot.send_message(message.chat.id, "Введите последние 4 цифры контактного номера заказчика:")
    bot.register_next_step_handler(msg, process_contact, user_data)

def process_contact(message, user_data):
    contact = message.text.strip()
    if len(contact) != 4 or not contact.isdigit():
        msg = bot.send_message(message.chat.id, "Неверный формат. Введите **последние 4 цифры** номера:")
        bot.register_next_step_handler(msg, process_contact, user_data)
        return
    user_data["contact"] = contact

    reservations = load_reservations()
    reservations[user_data["address"]] = {
        "user_id": message.from_user.id,
        "volume": user_data["volume"],
        "contact": user_data["contact"]
    }
    save_reservations(reservations)

    text = f"📌 Новая резервация:\nАдрес объекта: {user_data['address']}\nМатериал и количество: {user_data['volume']}\nКонтакт заказчика (последние 4 цифры номера): {user_data['contact']}"
    bot.send_message(GROUP_ID, text)
    bot.send_message(message.chat.id, "✅ Ваш объект успешно зарезервирован!", reply_markup=main_menu())


# ====== Запуск бота с защитой от крашей ======

print("Бот запущен...")

if __name__ == "__main__":
    while True:
        try:
            print("🚀 Polling стартует...")
            bot.infinity_polling(timeout=60, long_polling_timeout=90)
        except Exception as e:
            print(f"⚠️ Ошибка во время polling: {e}")
            print("⏱ Ждём 5 секунд и перезапускаем polling...")
            time.sleep(5)


