# Bellecroissant: каталог и заказы

Учебный Django REST API для товаров, клиентов и заказов. Для локального запуска нужен Python 3.13 и SQLite. Настройки из `.env.example` передаются как переменные окружения; файл `.env` автоматически не загружается.

```powershell
py -3.13 -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python manage.py migrate
.venv\Scripts\python manage.py runserver
```

JWT выдаётся через `/api/auth/jwt/create/`. Маршруты `/api/products/`, `/api/customers/`, `/api/orders/` требуют аутентификации. Заказ принимает `customer` и список `items` с `product` и положительным `quantity`; цену позиции сервер берёт из каталога. Статус меняется действиями `process`, `complete` и `cancel` у заказа.

```powershell
.venv\Scripts\python manage.py test --noinput
```

База `db.sqlite3` и байткод Python являются локальными артефактами. Для режима `DJANGO_DEBUG=0` требуется задать `DJANGO_SECRET_KEY`, допустимые `DJANGO_ALLOWED_HOSTS` и при необходимости CORS origins. Проект учебный; перед публичным размещением нужна отдельная проверка безопасности и конфигурации.
