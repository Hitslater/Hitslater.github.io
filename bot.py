from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import json, smtplib
from config import *

cart = {}

def start(update: Update, context: CallbackContext):
    user = update.effective_user.first_name
    update.message.reply_text(
        f"👋 Привет, {user}! Добро пожаловать в наш магазин. Напиши /menu чтобы начать."
    )

def menu(update: Update, context: CallbackContext):
    with open("products.json", "r") as f:
        products = json.load(f)
    text = "📋 Наши товары:\n\n"
    for product in products:
        text += f"{product['id']}. {product['name']} - {product['price']} грн\n"
    text += "\nНапиши номер товара, чтобы добавить в корзину."
    update.message.reply_text(text)

def handle_message(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    msg = update.message.text.strip()

    if msg.isdigit():
        prod_id = int(msg)
        with open("products.json", "r") as f:
            products = json.load(f)
        selected = next((p for p in products if p["id"] == prod_id), None)
        if selected:
            cart.setdefault(user_id, []).append(selected)
            update.message.reply_text(f"✅ {selected['name']} добавлен в корзину!")
        else:
            update.message.reply_text("❌ Товар не найден.")
    elif msg.lower() == "оформить":
        return checkout(update, context)
    else:
        update.message.reply_text("ℹ️ Напиши номер товара или 'Оформить' для завершения.")

def checkout(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    items = cart.get(user_id, [])
    if not items:
        update.message.reply_text("🛒 Ваша корзина пуста.")
        return

    total = sum(item['price'] for item in items)
    text = "🧾 Ваш заказ:\n"
    for item in items:
        text += f"- {item['name']} - {item['price']} грн\n"
    text += f"\n💰 Итого: {total} грн\n\n✉️ Отправляем заказ на почту..."

    update.message.reply_text(text)

    send_email(items, total)
    cart[user_id] = []

def send_email(items, total):
    body = "🧾 Новый заказ:\n"
    for item in items:
        body += f"- {item['name']} - {item['price']} грн\n"
    body += f"\n💰 Общая сумма: {total} грн"

    try:
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        message = f"Subject: Новый заказ\n\n{body}"
        server.sendmail(EMAIL_HOST_USER, EMAIL_RECEIVER, message)
        server.quit()
    except Exception as e:
        print("Ошибка отправки email:", e)

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("menu", menu))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()