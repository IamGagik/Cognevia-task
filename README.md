# Keycloak JWT Authentication API

Проект демонстрирует простую ролевую модель с использованием JWT токенов из Keycloak.

## Стэк технологий

- **FastAPI** (Python) - Backend API
- **Keycloak** - Identity and Access Management
- **PostgreSQL** - База данных для Keycloak
- **Docker Compose** - Оркестрация контейнеров

## Структура проекта

```
.
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py          # FastAPI приложение с эндпойнтами
│   │   ├── config.py        # Конфигурация
│   │   ├── security.py      # JWT валидация
│   │   └── dependencies.py  # FastAPI dependencies для проверки ролей
│   ├── Dockerfile
│   └── requirements.txt
├── docker_compose.yml
├── .env                     # Переменные окружения (создается из .env.example)
├── .env.example             # Шаблон переменных окружения
├── .gitignore
└── README.md
```

## Быстрый старт

### 1. Настройка переменных окружения

Создайте файл `.env` в корне проекта на основе `.env.example`:

```bash
cp .env.example .env
```

Отредактируйте `.env` файл при необходимости. Все конфигурационные данные (пароли, порты, realm и т.д.) находятся в этом файле.

### 2. Запуск сервисов

```bash
docker-compose up -d
```

Это запустит:
- PostgreSQL (порт из `.env`)
- Keycloak (порт из `.env`, по умолчанию 8080)
- FastAPI Backend (порт из `.env`, по умолчанию 8000)

### 3. Настройка Keycloak

После запуска Keycloak будет доступен по адресу: http://localhost:8080 (или порт из `.env`)

**Учетные данные администратора:**
- Username: из переменной `KEYCLOAK_ADMIN_USERNAME` в `.env` (по умолчанию `admin`)
- Password: из переменной `KEYCLOAK_ADMIN_PASSWORD` в `.env` (по умолчанию `admin`)

#### 3.1. Создание Realm

1. Войдите в админ-панель Keycloak
2. Наведите на выпадающий список в левом верхнем углу (обычно там "Master")
3. Нажмите "Create Realm"
4. Название: значение из `KEYCLOAK_REALM` в `.env` (по умолчанию `cognevia-realm`)
5. Нажмите "Create"

#### 3.2. Создание Client

1. В меню слева выберите "Clients"
2. Нажмите "Create client"
3. Client type: `OpenID Connect`
4. Client ID: значение из `KEYCLOAK_CLIENT_ID` в `.env` (по умолчанию `fastapi-client`)
5. Нажмите "Next"
6. Включите:
   - Client authentication: `ON`
   - Authorization: `OFF` (для упрощения)
   - Authentication flow: `Standard flow`
   - Direct access grants: `ON` (необходимо для password grant)
7. Valid redirect URIs: `*` (для демо)
8. Web origins: `*` (для демо)
9. Нажмите "Save"

#### 2.3. Настройка Client Secret

1. Откройте созданный client `fastapi-client`
2. Перейдите на вкладку "Credentials"
3. Скопируйте "Client secret" (понадобится для получения токенов)

#### 2.4. Создание ролей

1. В меню слева выберите "Realm roles"
2. Нажмите "Create role"
3. Создайте роль: `USER`
4. Нажмите "Create role" снова
5. Создайте роль: `ADMIN`

#### 2.5. Создание пользователей

**Пользователь с ролью USER:**

1. В меню слева выберите "Users"
2. Нажмите "Create new user"
3. Username: `testuser`
4. Email: `testuser@example.com`
5. First name: `user_first_name`
6. Last name: `user_last_name`
7. Включите "Email verified"
8. Нажмите "Create"
9. Перейдите на вкладку "Credentials"
10. Установите пароль (например: `password123`)
11. Отключите "Temporary" (чтобы пароль не требовал смены)
12. Нажмите "Save"
13. Перейдите на вкладку "Role mapping"
14. Нажмите "Assign role"
15. Выберите роль `USER`
16. Нажмите "Assign"

**Пользователь с ролью ADMIN:**

1. Создайте нового пользователя: `testadmin`
2. Email: `testadmin@example.com`
3. First name: `admin_first_name`
4. Last name: `admin_last_name`
5. Установите пароль (например: `password123`)
6. На вкладке "Role mapping" назначьте роль `ADMIN`

## API Эндпойнты

Все эндпойнты требуют заголовок `Authorization: Bearer <ACCESS_TOKEN>`

### GET /user/resource

Доступен для пользователей с ролью `USER`

**Ответы:**
- `200` - токен валиден и есть роль USER
- `401` - токен невалиден
- `403` - токен валиден, но нет роли USER

### GET /admin/resource

Доступен для пользователей с ролью `ADMIN`

**Ответы:**
- `200` - токен валиден и есть роль ADMIN
- `401` - токен невалиден
- `403` - токен валиден, но нет роли ADMIN

### GET /any/resource

Доступен для пользователей с ролью `ADMIN`

**Ответы:**
- `200` - токен валиден и есть роль ADMIN
- `401` - токен невалиден
- `403` - токен валиден, но нет роли ADMIN

## Получение токена

**Примечание:** В примерах ниже используются значения по умолчанию. В вашем случае используйте значения из файла `.env`:
- Порт Keycloak: `KEYCLOAK_PORT` (по умолчанию 8080)
- Realm: `KEYCLOAK_REALM` (по умолчанию cognevia-realm)
- Client ID: `KEYCLOAK_CLIENT_ID` (по умолчанию fastapi-client)


### Через Postman

1. Метод: POST
2. URL: `http://localhost:8080/realms/cognevia-realm/protocol/openid-connect/token`
   (или используйте значения из `.env`: `http://localhost:${KEYCLOAK_PORT}/realms/${KEYCLOAK_REALM}/protocol/openid-connect/token`)
3. Перейдите на вкладку "Body"
4. Выберите "x-www-form-urlencoded"
5. Добавьте следующие ключи и значения:
   - `username`: `testuser` (или `testadmin` для пользователя с ролью ADMIN)
   - `password`: `password123`
   - `grant_type`: `password`
   - `client_id`: `fastapi-client` (или значение из `KEYCLOAK_CLIENT_ID` в `.env`)
   - `client_secret`: `<ваш_client_secret>`
6. Нажмите "Send"
7. В ответе найдите поле `access_token` и скопируйте его значение

**Пример успешного ответа:**
```json
{
    "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
    "expires_in": 300,
    "refresh_expires_in": 1800,
    "refresh_token": "...",
    "token_type": "Bearer",
    "not-before-policy": 0,
    "session_state": "...",
    "scope": "profile email"
}
```

## Тестирование API через Postman

### Тестирование GET /user/resource

1. Создайте новый запрос
2. Метод: `GET`
3. URL: `http://localhost:8000/user/resource`
4. Перейдите на вкладку "Headers"
5. Добавьте заголовок:
   - Key: `Authorization`
   - Value: `Bearer <ваш_access_token>` (замените `<ваш_access_token>` на токен, полученный ранее)
6. Нажмите "Send"

**Ожидаемые результаты:**
- **200 OK** (если токен валиден и есть роль USER):
  ```json
  {
      "message": "Ваш токен валиден и есть роль USER",
      "roles": ["USER", ...]
  }
  ```
- **401 Unauthorized** (если токен невалиден или отсутствует)
- **403 Forbidden** (если токен валиден, но нет роли USER)

### Тестирование GET /admin/resource

1. Создайте новый запрос
2. Метод: `GET`
3. URL: `http://localhost:8000/admin/resource`
4. В заголовках добавьте:
   - Key: `Authorization`
   - Value: `Bearer <ваш_access_token>` (используйте токен пользователя с ролью ADMIN)
5. Нажмите "Send"

**Ожидаемые результаты:**
- **200 OK** (если токен валиден и есть роль ADMIN):
  ```json
  {
      "message": "Ваш токен валиден и есть роль ADMIN",
      "roles": ["ADMIN", ...]
  }
  ```
- **401 Unauthorized** (если токен невалиден)
- **403 Forbidden** (если токен валиден, но нет роли ADMIN)

### Тестирование GET /any/resource

1. Создайте новый запрос
2. Метод: `GET`
3. URL: `http://localhost:8000/any/resource`
4. В заголовках добавьте:
   - Key: `Authorization`
   - Value: `Bearer <ваш_access_token>` (используйте токен пользователя с ролью ADMIN)
5. Нажмите "Send"

**Ожидаемые результаты:**
- **200 OK** (если токен валиден и есть роль ADMIN)
- **401 Unauthorized** (если токен невалиден)
- **403 Forbidden** (если токен валиден, но нет роли ADMIN)


## Остановка сервисов

```bash
docker-compose down
```

Для удаления всех данных (включая базу данных):

```bash
docker-compose down -v
```

## Примечаниe

- Client secret можно найти в Keycloak Admin Console в разделе Clients → fastapi-client → Credentials