# АНРУС

Веб-приложение для расширения английского словарного запаса: общий словарь, личный словарь, тренировка перевода, тестирование и статистика пользователя.

## Возможности

- регистрация, вход и выход пользователей;
- общий словарь английских слов;
- поиск и фильтрация слов по уровню;
- проверка канонической формы английского слова при добавлении;
- личный словарь пользователя;
- добавление слов в личный словарь;
- отметка слов как изученных;
- тренировка перевода;
- тренировка перевода карточками до 10 слов за подход;
- тестирование по словам до 12 вопросов за попытку;
- сохранение результатов тестов;
- личный кабинет со статистикой;
- Django admin;
- адаптивная верстка;
- демо-данные;
- расширенный демо-словарь: 75 слов по уровням A1-C1;
- автотесты;
- документация и скриншоты в папке `docs`.

## Технологии

- Python 3.13;
- Django 5.2;
- inflect для проверки канонической формы английских слов;
- SQLite для локального запуска;
- HTML, CSS, JavaScript.

## Быстрый запуск

```bash
python -m venv venv
```

Активация виртуального окружения:

```bash
# Windows PowerShell
venv\Scripts\Activate.ps1

# Windows cmd
venv\Scripts\activate.bat

# macOS/Linux
source venv/bin/activate
```

Установка зависимостей, миграции и загрузка демо-данных:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py loaddata demo_data.json
python manage.py runserver
```

После запуска приложение доступно по адресу:

```text
http://127.0.0.1:8000/
```

## Демо-пользователь

После загрузки `demo_data.json` доступен учебный пользователь:

```text
Логин: demo_student
Пароль: DemoPass2026!
```

## Админ-панель

Админ-панель Django доступна по адресу:

```text
http://127.0.0.1:8000/admin/
```

Для создания администратора выполните:

```bash
python manage.py createsuperuser
```

## Автотесты

```bash
python manage.py test
```

## Демо-данные

Основной способ загрузки данных:

```bash
python manage.py loaddata demo_data.json
```

Также в проекте оставлена management-команда для повторного создания демо-набора:

```bash
python manage.py load_demo_words
```

## Структура проекта

```text
english_vocab_trainer/
├── english_vocab_trainer/       # настройки проекта Django
├── vocabulary/                  # приложение словаря и тренировок
│   ├── migrations/              # миграции базы данных
│   ├── management/commands/     # команда загрузки демо-слов
│   ├── templates/vocabulary/    # HTML-шаблоны
│   ├── admin.py                 # настройки Django admin
│   ├── forms.py                 # формы
│   ├── models.py                # модели данных
│   ├── tests.py                 # автотесты
│   ├── urls.py                  # маршруты приложения
│   └── views.py                 # представления
├── static/                      # CSS и JavaScript
├── docs/                        # скриншоты и материалы документации
├── demo_data.json               # фикстура с демо-данными
├── manage.py
├── requirements.txt
└── README.md
```

## Документация

В папке `docs` находятся:

- `docs/screenshots/` — скриншоты основных страниц;
- `docs/er_diagram.png` — ER-диаграмма;
- `docs/test_output.txt` — пример вывода автотестов.

## Деплой на Amvera Cloud

Проект подготовлен к деплою на Amvera Cloud через файл `amvera.yaml`.

1. Создайте приложение в Amvera Cloud.
2. Подключите GitHub-репозиторий проекта.
3. В разделе переменных добавьте:

```text
SECRET_KEY=любой_длинный_секретный_ключ
DEBUG=False
ALLOWED_HOSTS=.amvera.io,localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=https://*.amvera.io
```

4. Запустите сборку проекта.

При старте Amvera выполнит `start_amvera.py`: соберет статические файлы, применит миграции, загрузит демо-словарь и запустит Django через Gunicorn.

По умолчанию база SQLite хранится в `/data/db.sqlite3`. Это постоянное хранилище Amvera, поэтому данные не должны пропадать при пересборке приложения.

## Подготовка к публикации на GitHub

В репозиторий не нужно добавлять локальные и временные файлы:

- `venv/`;
- `db.sqlite3`;
- `__pycache__/`;
- `.env`;
- `.pytest_cache/`.

Эти файлы и папки уже указаны в `.gitignore`.


:)
