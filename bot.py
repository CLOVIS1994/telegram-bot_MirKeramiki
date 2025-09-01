# -*- coding: utf-8 -*-

import telebot
from telebot import types
import time
import os

# Токен берём из переменных окружения Railway
TOKEN = os.environ.get("BOT_TOKEN") or "7628596509:AAH-GgXWnMJlUUs9mMPr9PRiy-gRr6h3AYY"
bot = telebot.TeleBot(TOKEN)

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("📄 Скачать прайс-листы"))
    markup.add(types.KeyboardButton("📷 Галерея Toza Marković"))
    markup.add(types.KeyboardButton("🌐 Перейти на сайт"))
    markup.add(types.KeyboardButton("🎉 Актуальные акции"))
    markup.add(types.KeyboardButton("📞 Контакты"))
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
        time.sleep(2)

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

    else:
        bot.send_message(message.chat.id, "Неизвестная команда. Выберите из меню ниже 👇", reply_markup=main_menu())

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
