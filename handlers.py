from main import bot
from keyboards import keyboard
from aiogram import types
from aiogram.dispatcher.filters import Command
import json

# Временное хранилище корзины
cart = {}  # {chat_id: [{"id": str, "quantity": int}, ...]}

PRICE = {
    '1': [types.LabeledPrice(label='Item1', amount=1500)],  # Суммы в копейках (15 RUB = 1500)
    '2': [types.LabeledPrice(label='Item2', amount=1500)],
    '3': [types.LabeledPrice(label='Item3', amount=2100)],
    '4': [types.LabeledPrice(label='Item4', amount=5000)],
    '5': [types.LabeledPrice(label='Item5', amount=1800)],
    '6': [types.LabeledPrice(label='Item6', amount=500)]
}

async def start(message: types.Message):
    print(f"Received /start from {message.chat.id}")  # Логирование
    await bot.send_message(message.chat.id, 'Тестируем WebApp!', reply_markup=keyboard)

async def buy_process(web_app_message: types.Message):
    chat_id = web_app_message.chat.id
    try:
        # Парсим данные из Web App
        data = json.loads(web_app_message.web_app_data.data)
        items = data.get("items", [])

        # Сохраняем корзину
        cart[chat_id] = items

        # Формируем список цен для счёта
        prices = []
        for item in items:
            item_id = item["id"]
            quantity = item["quantity"]
            if item_id in PRICE:
                price = PRICE[item_id][0]
                prices.append(
                    types.LabeledPrice(
                        label=f"{price.label} (x{quantity})",
                        amount=price.amount * quantity
                    )
                )

        if not prices:
            await bot.send_message(chat_id, "Корзина пуста!")
            return

        # Отправляем счёт
        await bot.send_invoice(
            chat_id,
            title='Покупка товаров',
            description='Оплата выбранных товаров',
            provider_token='PAYMENTS_TOKEN',  # Замените на реальный токен
            currency='RUB',
            need_email=True,
            prices=prices,
            start_parameter='example',
            payload='cart_invoice'
        )
    except json.JSONDecodeError:
        await bot.send_message(chat_id, "Ошибка в данных корзины!")

async def pre_checkout_process(pre_checkout: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout.id, ok=True)

async def successful_payment(message: types.Message):
    chat_id = message.chat.id
    if chat_id in cart:
        del cart[chat_id]
    await bot.send_message(chat_id, 'Платеж прошел успешно! Спасибо за покупку!')

async def view_cart(message: types.Message):
    chat_id = message.chat.id
    if chat_id not in cart or not cart[chat_id]:
        await bot.send_message(chat_id, "Корзина пуста!")
        return
    response = "Ваша корзина:\n"
    total = 0
    for item in cart[chat_id]:
        item_id = item["id"]
        quantity = item["quantity"]
        price = PRICE[item_id][0]
        response += f"{price.label} (x{quantity}): {price.amount * quantity / 100} RUB\n"
        total += price.amount * quantity
    response += f"\nИтого: {total / 100} RUB"
    await bot.send_message(chat_id, response)

async def clear_cart(message: types.Message):
    chat_id = message.chat.id
    if chat_id in cart:
        del cart[chat_id]
        await bot.send_message(chat_id, "Корзина очищена!")
    else:
        await bot.send_message(chat_id, "Корзина уже пуста!")