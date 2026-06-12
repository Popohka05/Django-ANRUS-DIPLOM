# Деплой в Yandex Cloud через виртуальную машину

Этот способ подходит для демонстрации дипломного проекта: приложение запускается в Docker-контейнере на виртуальной машине Yandex Compute Cloud и открывается по публичному IP-адресу.

## 1. Создание виртуальной машины

1. Откройте Yandex Cloud Console.
2. Создайте виртуальную машину в сервисе Compute Cloud.
3. Рекомендуемые параметры:
   - образ: Ubuntu 24.04 LTS или Ubuntu 22.04 LTS;
   - vCPU: 2;
   - RAM: 2 ГБ;
   - диск: 20 ГБ;
   - публичный IP: включить;
   - доступ по SSH: добавить свой SSH-ключ.
4. В группе безопасности откройте входящие порты:
   - `22` для SSH;
   - `80` для сайта.

## 2. Подключение к серверу

```bash
ssh <user>@<public-ip>
```

## 3. Установка Docker

```bash
sudo apt update
sudo apt install -y ca-certificates curl git docker.io docker-compose-plugin
sudo systemctl enable --now docker
```

## 4. Загрузка проекта

```bash
git clone https://github.com/Popohka05/Django-ANRUS-DIPLOM.git
cd Django-ANRUS-DIPLOM
```

## 5. Настройка переменных окружения

Создайте файл `.env`:

```bash
nano .env
```

Добавьте:

```text
SECRET_KEY=replace_this_with_long_random_key
ALLOWED_HOSTS=*
CSRF_COOKIE_SECURE=False
SESSION_COOKIE_SECURE=False
```

Для генерации ключа можно выполнить:

```bash
python3 - <<'PY'
import secrets
import string
chars = string.ascii_letters + string.digits + '_'
print(''.join(secrets.choice(chars) for _ in range(64)))
PY
```

## 6. Запуск приложения

```bash
sudo docker compose up -d --build
```

Проверка логов:

```bash
sudo docker compose logs -f
```

## 7. Открытие сайта

Откройте в браузере:

```text
http://<public-ip>/
```

Админ-панель:

```text
http://<public-ip>/admin/
```

Демо-пользователь:

```text
demo_student
DemoPass2026!
```

## Полезные команды

Остановить приложение:

```bash
sudo docker compose down
```

Пересобрать после обновления кода:

```bash
git pull
sudo docker compose up -d --build
```

Посмотреть запущенные контейнеры:

```bash
sudo docker ps
```
