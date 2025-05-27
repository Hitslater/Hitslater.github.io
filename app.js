let tg = window.Telegram.WebApp;

tg.expand();

tg.MainButton.textColor = '#FFFFFF';
tg.MainButton.color = '#2cab37';

// Список товаров (соответствует PRICE в handlers.py и index.html)
const items = [
    { id: "1", name: "Амарант (червоний)", price: 15 },
    { id: "2", name: "Кокосовый субстрат 5 кг", price: 15 },
    { id: "3", name: "Горох", price: 21 },
    { id: "4", name: "Кинза", price: 50 },
    { id: "5", name: "Редис (sango)", price: 18 },
    { id: "6", name: "Рукола", price: 5 }
];

let cart = [];

// Получение кнопок
let btn1 = document.getElementById("btn1");
let btn2 = document.getElementById("btn2");
let btn3 = document.getElementById("btn3");
let btn4 = document.getElementById("btn4");
let btn5 = document.getElementById("btn5");
let btn6 = document.getElementById("btn6");

// Добавление в корзину
function addToCart(itemId) {
    const existing = cart.find(i => i.id === itemId);
    if (existing) {
        existing.quantity += 1;
    } else {
        cart.push({ id: itemId, quantity: 1 });
    }
    updateCartDisplay();
    tg.MainButton.setText(`Оформить заказ (${cart.length} товаров)`);
    tg.MainButton.show();
}

// Обработчики кнопок
btn1.addEventListener("click", () => addToCart("1"));
btn2.addEventListener("click", () => addToCart("2"));
btn3.addEventListener("click", () => addToCart("3"));
btn4.addEventListener("click", () => addToCart("4"));
btn5.addEventListener("click", () => addToCart("5"));
btn6.addEventListener("click", () => addToCart("6"));

// Обновление отображения корзины
function updateCartDisplay() {
    const cartDiv = document.getElementById("cart");
    cartDiv.innerHTML = "";
    if (cart.length === 0) {
        cartDiv.innerHTML = "Корзина пуста";
        tg.MainButton.hide();
        return;
    }
    let total = 0;
    cart.forEach(item => {
        const itemInfo = items.find(i => i.id === item.id);
        const itemTotal = itemInfo.price * item.quantity;
        total += itemTotal;
        const div = document.createElement("div");
        div.innerHTML = `${itemInfo.name} (x${item.quantity}) - ${itemTotal} RUB`;
        cartDiv.appendChild(div);
    });
    const totalDiv = document.createElement("div");
    totalDiv.innerHTML = `<strong>Итого: ${total} RUB</strong>`;
    cartDiv.appendChild(totalDiv);
}

// Отправка корзины
Telegram.WebApp.onEvent("mainButtonClicked", function() {
    if (cart.length === 0) {
        tg.showAlert("Корзина пуста!");
        return;
    }
    tg.sendData(JSON.stringify({ items: cart }));
});

// Отображение имени пользователя
let usercard = document.getElementById("usercard");
let p = document.createElement("p");
p.innerText = `${tg.initDataUnsafe.user?.first_name || ''} ${tg.initDataUnsafe.user?.last_name || ''}`;
usercard.appendChild(p);

// Инициализация
updateCartDisplay();
