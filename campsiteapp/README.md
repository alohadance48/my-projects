# CampSiteApp

Проект для управления пользователями, комментариями, бронированием и сменами для лагеря. Система защищена через Keycloak и использует Django Rest Framework.

## Оглавление

1. [Описание проекта](#Описание-проекта)
2. [Основные Маршруты](#Основные-маршруты)
3. [Документация API c curl](#Документация-api)
   - [Авторизация](#Авторизация-в-админ-панель)
   - [Регистрация нового администратора](#API-для-регистрации-нового-админа)
   - [Удаление администратора](#API-для-удаления-администратора)
   - [Выход из системы admin](#Выход-из-системы-админов)
   - [Выход из системы keycloak](#Выход-из-Keycloak)
   - [Получение данных о пользователе](#Получение-данных-о-пользователе)
   - [Бронирование](#Бронирование)
   - [Просмотр и добавление комментариев](#просмотр-и-добавление-комментариев-и-их-удаление)
   - [Смена лагеря](#Смена-лагеря-и-удаление-с-обновлением)
   - [Смена лагеря(с картинками)](#Создание-смены-с-фото)
   - [Обновление количества мест](#Обновление-количества-мест-на-смену)
   - [Подтверждение бронирования](#Подтверждение-брони)
   - [Регистрация пользака в keyclaok](#Регистрация-пользователя-в-keycloak)
   - [Авторизация в keycloak](#Авторизация-в-keycloak)
4. [Коллекция Postman](#Postman)
5. [Установка и запуск App](#Установка)
6. [Основной функционал Админки](#Основной-функционал-админки)
7. [Безопасность](#Безопасность)

## Описание проекта

Это приложение разработано для управления лагерем. Оно включает в себя несколько API для взаимодействия с пользователями, админами, бронированиями и комментариями. Система использует Keycloak для аутентификации и авторизации.

## Основные Маршруты

### Аутентификация
- `POST /api/v1/registr/` - Регистрация через Keycloak
- `POST /api/v1/login/keycloak/` - Авторизация через Keycloak
- `GET /api/me/v1/keycloak/` - Данные пользователя Keycloak
- `GET /api/v1/logout/` - Выход из Keycloak
- `POST /api/v1/admin/login/` - Авторизация в админку (DRF Token)
- `POST /api/v1/admin/logout/` - Выход из админки

### Смены лагеря
- `GET /api/v1/datecamp/` - Все смены
- `POST /api/v1/admin/datecamp/` - Создание смены
- `PATCH /api/v1/admin/` - Обновление смены
- `DELETE /api/v1/admin/` - Удаление смены
- `POST /api/v1/admin/dateplaces/` - Обновление количества мест

### Бронирование
- `POST /api/v1/user/booking/` - Создание брони
- `GET /api/v1/admin/bookings/` - Все брони (админ)
- `PUT /api/v1/admin/update/status/bookings/` - Обновление статуса брони
- `DELETE /api/v1/admin/bookings/delete/` - Удаление брони
### Комментарии
- `GET /api/v1/allcomments/` - Все комментарии
- `POST /api/v1/comment/leave/` - Создание комментария
### Пользователи
- `GET /api/v1/me/` - Данные текущего пользователя (DRF Token)
- `GET /api/v1/admin/alladmin/` - Все администраторы
## Документация API

### Авторизация в keycloak
#### Маршрут 
```angular2html
api/v1/login/keycloak/
```
#### json 
```json
{
  "username": "username",
  "password": "password"
}
```
#### curl 
```bash 
curl -X POST https://your-backend.com/api/v1/login/keycloak/ \
  -H "Content-Type: application/json" \
  -d '{"username": "your_username", "password": "your_password"}'
```

### Регистрация пользователя в keycloak
#### json 
```json
{
    "username": "your_username",
    "email": "your_email@example.com",
    "password": "your_strong_password"
  }
```


#### curl 
```bash 
curl -X POST 'http://localhost:8000/api/v1/registr/' \
  -H "Content-Type: application/json" \
  -d '{
    "username": "your_username",
    "email": "your_email@example.com",
    "password": "your_strong_password"
  }'
```


### Авторизация в админ-панель

**POST** `/api/v1/login/admin/`
Для авторизации в админ-панель, отправьте логин и пароль.

### json 
```json
{
  "username": "root",
  "password": "]b\q,W^G$[DTvi]fZ7FAN?6:ipdg?jgMQo@S)3:–"
}
```
### curl 

``` bash
curl -X POST http://127.0.0.1:8000/api/v1/admin/login/ \
-H "Content-Type: application/json" \
-d '{"username": "root", "password": "]b\\q,W^G$[DTvi]fZ7FAN?6:ipdg?jgMQo@S)3:–"}'
```

#### Ответ (его надо сохранять, он будет разный, тут показан примерный формат):
``` json
}
"token": "fe51a193338ad1f869e757fe5ae59eb0c15f571c"
}
```
#### Ответ (Ошибка)
```json
{
    "non_field_errors": ["Неверные данные!"]
}

```

#### API для регистрации нового админа
#### json 

```json
{
  "username": "root_user11111",
  "email": "root@example.com",
  "password": "supersecurepassword",
  "is_staff": true
}
```
#### curl 
```bash 
curl -X POST http://localhost:8000/api/v1/admin/ \
  -H "Authorization: Token <ВАШ_DRF_ТОКЕН_РУТА>" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin2@example.com",
    "password": "supersecret",
    "username": "admin2"
  }'
```
#### Ответ (Успех)
```json
{
    "username": "newuser",
    "first_name": "John",
    "last_name": "Doe",
    "email": "newuser@example.com"
}
```
#### Ответ (ошибка)
```json
{
    "email": ["Пользователь с таким email уже существует."]
}

```

### API для удаления администратора
#### json
```json
{
  "email": "admin@example.com"
}

```
#### curl 
```bash 
curl -X DELETE 'http://localhost:8000/api/v1/admin/' \
-H 'Authorization: Token <ROOT_TOKEN>' \
-H 'Content-Type: application/json' \
-d '{"email": "admin@example.com"}'
```
#### Ответ(Успех)
```json
{
  "message": "Пользователь успешно удален!"
}
```
#### Ответ(Ошибка, когда нет email)
```json
{
    "error": "Email Обязателен!"
}

```
#### Ответ(Ошибка, когда нет прав, не от root)
```json
{
   "error": "Email Обязателен!"
}
```
### Выход из системы админов
#### curl 
```bash 
curl -X POST "http://localhost:8000/api/v1/logout/admin" \
    -H "Authorization: Token db53c92b242b99b9e8a46dec0f4d3c6f1e014183"
```
#### Ответ (Успех)
```json
{
    "detail": "You have been logged out."
}

```
#### Ответ(ошибка)
```json
{
    "detail": "You have been logged out."
}
```
### Выход из Keycloak
#### curl 
```bash 
curl -X POST "http://localhost:8000/api/v1/logout/" \
    -H "Authorization: Token 1234567890abcdef"
```
#### Ответ (Успех)
```json
{
    "message": "You have been logged out successfully."
}
```
### Получение данных о пользователе
#### curl 
```bash 
curl -X GET "http://localhost:8000/api/v1/me/" \
    -H "Authorization: Token 428b611a495b610ed86c2b8e605417c6b397cf4a"
```
#### Ответ(Успешно)
```json
{
    "user": "admin",
    "email": "admin@example.com",
    "is_staff": true,
    "is_root": true
}
```
#### Ответ(Ошибка 401)
```json
{
    "detail": "Authentication credentials were not provided."
}
```
#### Ответ(Ошибка 403)
```json
{
    "detail": "You do not have permission to perform this action."
}
```
#### Ответ(Ошибка 400)
```json
{
    "detail": "Token is missing or invalid."
}
```
### Бронирование
#### curl 
```bash
curl -X POST 'http://localhost:8000/api/v1/user/booking/' \
-H 'Authorization: Bearer <KEYCLOAK_TOKEN>' \
-H 'Content-Type: application/json' \
-d '{
  "date_camp": 1,
  "surname_parent": "Иванов",
  "name_parent": "Иван",
  "patronymic_parent": "Иванович",
  "email_parent": "ivanov@example.com",
  "number_parent": "+79991234567",
  "series_passport_parent": "1234567890",
  "issued_passport_parent": "Отделением УФМС Москвы",
  "date_of_issue": "2015-06-15",
  "registration_address_parent": "г. Москва, ул. Пушкина, д. 10, кв. 5",
  "surname_child": "Иванова",
  "name_child": "Мария",
  "patronymic_child": "Ивановна",
  "date_of_birth": "2010-04-20",
  "address_child": "г. Москва, ул. Пушкина, д. 10, кв. 5"
}'
```
#### Ответ(Успех)
#### json 
```json
{
    "message": "Ваша бронь оставлена!"
}
```
#### Ответ(Ошибка 400)
#### 1.
```json
{
    "surname_parent": ["Это поле обязательно."],
    "email_parent": ["Введите корректный email."],
    "series_passport_parent": ["Введите 10 цифр: 4 серии и 6 номера без пробелов."]
}
```
#### 2.
```json
{
    "detail": "Внутренняя ошибка сервера. Попробуйте позже."
}

```
### Просмотр и добавление комментариев и их удаление
#### Просмотр(curl)

```bash 
curl -X GET http://127.0.0.1:8000/api/v1/comment/ \
```
#### Ответ(Успешный)
```json
[
    {
        "id": 1,
        "text": "Отличный лагерь!",
        "created_at": "2025-05-06T14:30:00Z"
    },
    {
        "id": 2,
        "text": "Очень понравилось! Спасибо!",
        "created_at": "2025-05-06T15:00:00Z"
    }
]

```
#### Ответ(Ошибка)
```json
{
  "error": "Internal Error"
}

```
#### Добавление комментария 
#### curl 
```bash 
curl -X POST 'http://localhost:8000/api/v1/comment/leave/' \
-H 'Authorization: Bearer <KEYCLOAK_TOKEN>' \
-H 'Content-Type: application/json' \
-d '{"text": "Отличный лагерь!", "stars": 5}'

```
#### Ответ (успех)
```json
{
  "id": 1,
  "text": "Отличный лагерь!",
  "created_at": "2025-05-29T12:30:45Z",
  "stars": 5,
  "username": "ivanov"
}

```
#### Удаление комментов
#### curl 
```bash 
curl -X DELETE http://localhost:8000/api/v1/admin/ \
  -H "Authorization: Token <ВАШ_DRF_ТОКЕН_РУТА>" \
  -H "Content-Type: application/json" \
  -d '{"comment_id": 1}'
```
#### Ответ
```angular2html
204 No Content
```
### Смена лагеря и удаление с обновлением
#### curl 
```bash 
curl -X PATCH http://localhost:8000/api/v1/admin/ \
  -H "Authorization: Token <ВАШ_DRF_ТОКЕН>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "summer_2025",
    "places": 60,
    "price": 17000
  }'
```
#### Ответ(Успех)
```json

{
  "id": 5,
  "name": "summer_2025",
  "full_name": "Полное название смены 5",
  "part": "3",
  "date": "2025-07-10",
   "places": "60",
   "price": "17000",
   "text": "Описание смены."
}

```
#### Ответ(Ошибка 400)
#### Код
```angular2html
400 Bad Request
Content-Type: application/json
```


#### json
```json
  {
  "error": "Поле 'id' обязательно для обновления"
}
```
### Добавление новой смены лагеря
```bash 
curl -X POST 'http://localhost:8000/api/v1/admin/datecamp/' \
  -H "Authorization: Token <ВАШ_DRF_ТОКЕН>" \
  -F 'name=summer_2025' \
  -F 'full_name=Летняя смена 2025' \
  -F 'part=Первая часть' \
  -F 'date=2025-07-01' \
  -F 'places=50' \
  -F 'price=15000' \
  -F 'text=Описание летней смены'

```

#### Ответ(Успех)
```json

{
"id":5,
"name":"Летняя смена 2025",
"full_name":"sdfsd",
"part": "Первая часть", 
   "date": "2025-07-01",
    "places": 50,
    "price": 15000,
    "text": "Описание летней смены"
  }
```
#### Ответ(Ошибка 400)
#### Код
```angular2html
400 Bad Request
Content-Type: application/json
```
``` angular2html
   {"error":"Неизвестная операция или неверные данные"}
```

### Создание смены с фото
#### curl 
```bash 
curl -X POST 'http://localhost:8000/api/v1/admin/datecamp/' \
-H 'Authorization: Token <ADMIN_TOKEN>' \
-F 'name=Summer2025' \
-F 'full_name=Летняя смена 2025' \
-F 'part=1' \
-F 'date=2025-06-15' \
-F 'places=50' \
-F 'price=20000' \
-F 'text=Описание смены' \
-F 'image=@summer.jpg'
```

## Подтверждение брони

### curl 
```bash 
curl -X PUT http://localhost:8000/api/booking/update-status/ \
  -H "Content-Type: application/json" \
  -d '{
        "username": "testuser",
        "date_camp": "1",
        "status": True 
      }'

```
## Удаление неподтверждённой брони

### curl 
```bash 
curl -X DELETE http://127.0.0.1:8000/api/v1/admin/bookings/delete/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token <ваш_админ_токен>" \
  -d '{"id": "3"}'

```

### json 
```json 
{
  "id": "3"
}

```
### Обновление количества мест на смену
#### json 
```json 
{
   "name": "Summer2025", 
   "operation": "inc"
}
```
#### curl
```bash 
curl -X POST 'http://localhost:8000/api/v1/admin/dateplaces/' \
-H 'Authorization: Token <ADMIN_TOKEN>' \
-H 'Content-Type: application/json' \
-d '{"name": "Summer2025", "operation": "inc"}'
```



## Установка
1. Создание venv и установка библиотек 
```bash 
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
2. Запуск backend 
```bash
python manage.py makemigrations
python manage migrate 
python manage runserver
```
3. Запуск kyecloak 
```bash
bin/kc.sh start-dev
```


### POSTMAN
[JSON-файл](./postman.json)

## Основной функционал админки
#### Админка (api/v1/admin/)
1. Просмотр всех админов 
2. Создание обновление и удаление смен 
3. Удаление отзывов cd 
4. Подтверждение броней путевок 
5. Обновление мест на смену 
6. Создание и удаление админов 
7. Просмотр всех оставленных броней(включая данные человека)
8. logout 

---

## 🔐 Аутентификация

Эндпоинт не требует авторизации, но использует `client_credentials` токен от **административного клиента Keycloak**, чтобы иметь право создавать пользователей.

---

## 📥 Тело запроса (JSON)

```json
{
  "username": "exampleuser",
  "email": "user@example.com",
  "password": "StrongPassword123!"
}
```

## Безопасность

### Документация по самописной системе "Время жизни drf-token"

#### Настройка времени жизни:
```python
TOKEN_EXPIRE_TIME = 900
```

#### Проверка времени жизни:
```python
user, token = super().authenticate_credentials(key)
expiration_time = token.created + timedelta(seconds=self.TOKEN_EXPIRE_TIME)
    if expiration_time < now():
        token.delete()
        raise AuthenticationFailed('Token has expired')
```

### Логика работы

1. Получает токен
2. Проверяет время жизни
3. Удаляет если истекло время жизни 

#### Особенность 
- Нет прямого curl, система будет работать сама.

### Описание drf-token 

- Длина: 40 символов 
- Время жизни: True 
- Наличие ролей: True 


