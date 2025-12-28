import os
import telebot
import time
import requests
import sys

TOKEN = os.environ.get('BOT_TOKEN')
if not TOKEN:
    print("❌ BOT_TOKEN не найден!")
    sys.exit(1)

print("=" * 50)
print("🔄 ПРИНУДИТЕЛЬНЫЙ СБРОС СОЕДИНЕНИЙ...")

# 1. Удаляем webhook
try:
    print("1. Удаляю webhook...")
    url = f"https://api.telegram.org/bot{TOKEN}/deleteWebhook"
    response = requests.get(url, timeout=10)
    print(f"   Результат: {response.json()}")
except Exception as e:
    print(f"   Ошибка: {e}")

time.sleep(2)

# 2. Сбрасываем offset
try:
    print("2. Сбрасываю offset...")
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates?offset=999999999"
    response = requests.get(url, timeout=10)
    print(f"   Результат: {response.json()}")
except Exception as e:
    print(f"   Ошибка: {e}")

time.sleep(3)

print("✅ Сброс завершён. Жду 5 секунд...")
time.sleep(5)

print("=" * 50)
print("🤖 СОЗДАЮ БОТА...")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "✅ Бот работает после сброса конфликта!")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Вы сказали: {message.text}")

print("🚀 ЗАПУСКАЮ POLLING...")
print("=" * 50)

# Запускаем с несколькими попытками
max_attempts = 5
for attempt in range(max_attempts):
    try:
        print(f"\nПопытка {attempt + 1}/{max_attempts}...")
        bot.polling(none_stop=True, skip_pending=True, interval=3, timeout=30)
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        if "409" in str(e):
            print("Обнаружен конфликт. Жду 10 секунд и пробую снова...")
            time.sleep(10)
            if attempt < max_attempts - 1:
                continue
        print("🛑 Бот остановлен.")
        break
