
# -*- coding: utf-8 -*-

import telebot
from telebot import types
import time
import os

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

        files = ["Прайс_общестрой.xlsx", "Прайс_кровельный.xls"]  # список файлов для отправки
        for filename in files:
            try:
                with open(filename, "rb") as f:
                    bot.send_document(message.chat.id, f)
                    time.sleep(1)
            except FileNotFoundError:
                bot.send_message(message.chat.id, f"❌ Файл {filename} не найден. Пожалуйста, добавьте его рядом с bot.py", reply_markup=main_menu())

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
            bot.send_message(message.chat.id, "❌ Картинка с акцией не найдена. Поместите файл promo.jpg рядом с bot.py", reply_markup=main_menu())

    elif message.text == "📞 Контакты":
        contacts_text = (
            "📍 *Наши контакты:*\n\n"
            "🏢 *Офис*\n"
            "📞 +380503909383 (Олег Баранов - общестрой)\n"
            "📞 +380979560464 (Евгений Рогачко - кровля)\n"
            "📍 [г. Одесса, ул. Левитана 62](https://www.google.com/maps/place/Мир+Керамики+-+строительные+материалы+в+Одессе+и+области/@46.4075791,30.7221186,17z/data=!3m1!4b1!4m6!3m5!1s0x40c63337397bfa2b:0xcec13337eb49ba2d!8m2!3d46.4075791!4d30.7221186!16s%2Fg%2F11gm8szrpg?hl=en-RO&entry=ttu&g_ep=EgoyMDI1MDgwNi4wIKXMDSoASAFQAw%3D%3D)\n\n"
            "🏢 *Склад №1*\n"
            "📞 +380950411490 (кладовщик Андрей)\n"
            "📍 [г. Одесса, Киевское шоссе 2](https://www.google.com/maps/place/Строительные+товары+Мир+Керамики+2/@46.4905258,30.6747304,17z/data=!3m1!4b1!4m6!3m5!1s0x40c62f3a4807c915:0xc608fcc842012efd!8m2!3d46.4905258!4d30.6747304!16s%2Fg%2F11rwqq7jsl?hl=en-RO&entry=ttu&g_ep=EgoyMDI1MDgwNi4wIKXMDSoASAFQAw%3D%3D)\n\n"
            "🏢 *Склад №2*\n"
            "📞 +380505190818 (кладовщик Вадим)\n"
            "📍 [с. Нерубайское, Пастера 1](https://www.google.com/maps/place/Строительные+материалы+Мир+Керамики/@46.5356156,30.6386978,17z/data=!4m6!3m5!1s0x40c62fdca68102f1:0x760153ce75529fab!8m2!3d46.5356155!4d30.6426207!16s%2Fg%2F11n_z7l9wz?hl=en-RO&entry=ttu&g_ep=EgoyMDI1MDgwNi4wIKXMDSoASAFQAw%3D%3D)"
            )

        # <-- ОТСЮДА БЫЛО НЕДОСТАЮЩЕЕ ОТПРАВЛЕНИЕ
        bot.send_message(
            message.chat.id,
            contacts_text,
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=main_menu()
        )

    else:
        bot.send_message(message.chat.id, "Неизвестная команда. Пожалуйста, выберите действие из меню.", reply_markup=main_menu())

print("Бот запущен...")
bot.polling(none_stop=True)
