# SauceDemo — Selenium + pytest + Page Object Model

Автотесты для [saucedemo.com](https://www.saucedemo.com/): логин, каталог, корзина,
чекаут. Портфолио-проект, демонстрирующий подход к автоматизации UI-тестирования:
Page Object Model, явные ожидания, параметризованные тесты, HTML-отчёты,
CI на GitHub Actions.

Automated UI tests for [saucedemo.com](https://www.saucedemo.com/) covering login,
inventory, cart and checkout flows. A portfolio project demonstrating the Page
Object Model, explicit waits, parametrized tests, HTML reporting and CI on
GitHub Actions.

## Стек / Stack

- Python 3.11
- Selenium WebDriver 4.x (Selenium Manager — драйвер браузера подтягивается
  автоматически, ничего вручную скачивать не нужно)
- pytest + pytest-html
- GitHub Actions (запуск тестов на каждый push/PR, HTML-отчёт как артефакт)

## Структура / Structure

```
config.py              # базовый URL, тестовые пользователи, таймауты
conftest.py             # фикстура driver, скриншот в отчёт при падении теста
pages/                  # Page Object классы
  base_page.py
  login_page.py
  inventory_page.py
  cart_page.py
  checkout_page.py
tests/
  test_login.py         # успешный вход, locked_out_user, неверный пароль, пустые поля
  test_inventory.py      # каталог, корзина-бейдж, сортировка, баг problem_user
  test_cart.py           # состав корзины, удаление, edge case с пустой корзиной
  test_checkout.py       # полный сценарий покупки + валидация обязательных полей
```

## Что покрыто тестами / What's covered

Не только happy path — специально включены негативные и граничные случаи:

- неверный пароль / заблокированный пользователь / пустые поля логина
- сортировка каталога по цене и по имени в обе стороны
- визуальный баг `problem_user` (одинаковая картинка у всех товаров) — тест как
  регрессионный guard, а не как баг-репорт
- переход в чекаут с пустой корзиной
- валидация каждого обязательного поля на шаге оформления заказа отдельно
- сверка Item total + Tax == Total на странице подтверждения заказа

## Запуск / Run locally

```bash
pip install -r requirements.txt
pytest                     # по умолчанию headless, отчёт в reports/report.html
HEADLESS=0 pytest           # с видимым браузером
```

## CI

Тесты гоняются на GitHub Actions при каждом push и pull request в `main`,
HTML-отчёт сохраняется как artifact сборки.

---

