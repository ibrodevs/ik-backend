# IK Backend (Django + DRF)

REST API для новостей, достопримечательностей, отделов и медиа.

## Стек
- Django 4.2
- Django REST Framework
- PostgreSQL (на Heroku)

## Запуск локально
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
DEBUG=True python manage.py migrate
DEBUG=True python manage.py runserver
```

## Тестовые данные
Команда заполняет все сущности тестовыми данными (категории, новости, отделы, руководители, достопримечательности, галерея, медиа):

```bash
DEBUG=True python manage.py seed_test_data
```

## Деплой в Heroku
```bash
heroku login
heroku git:remote -a ik-backend-780b39b1dc1f
heroku config:set SECRET_KEY='your-secret' DEBUG=False
heroku config:set ALLOWED_HOSTS='ik-backend-780b39b1dc1f.herokuapp.com'
heroku config:set CORS_ALLOWED_ORIGINS='https://issyk-kul.vercel.app,http://localhost:5173'
git push heroku main
heroku run python manage.py seed_test_data
```

## API
Base URL: `/api/`

Язык локализации через заголовок `Accept-Language: ru|en|kg`.

### Auth
`POST /api/auth/token/`

Request:
```json
{
  "username": "admin",
  "password": "admin"
}
```

Response:
```json
{
  "token": "<auth_token>"
}
```

### News
`GET /api/news/`  
Параметры: `category_id`, `is_hot=true|false`, `is_main=true|false`

Response item:
```json
{
  "id": 1,
  "title": "Главная новость проекта",
  "short_description": "Тестовый анонс новости.",
  "description": "Тестовое полное описание новости.",
  "date": "2026-02-27T10:00:00Z",
  "category": {
    "id": 1,
    "name": "Официально"
  },
  "image": "https://<host>/media/news/news_image_xxx.png",
  "is_hot": true,
  "is_main": true
}
```

`GET /api/news/{id}/` - тот же формат одного объекта.

### News categories
`GET /api/news-categories/`

Response item:
```json
{
  "id": 1,
  "name": "Официально",
  "slug": "official",
  "order": 1
}
```

`GET /api/news-categories/{id}/` - тот же формат одного объекта.

### Sights
`GET /api/sights/`

Response item:
```json
{
  "id": 1,
  "title": "Озеро Иссык-Куль",
  "short_description": "Тестовое описание достопримечательности.",
  "description": "Подробное тестовое описание достопримечательности.",
  "main_image": "https://<host>/media/sights/main/sight_main_xxx.png",
  "gallery": [
    {
      "id": 1,
      "title": "Галерея 1-1",
      "image": "https://<host>/media/sights/gallery/sight_gallery_xxx.png",
      "order": 1
    }
  ]
}
```

`GET /api/sights/{id}/` - тот же формат одного объекта.

### Departments
`GET /api/departments/`  
Параметры: `category_id`

Response item:
```json
{
  "id": 1,
  "icon": "https://<host>/media/departments/icons/department_icon_xxx.png",
  "title": "Отдел стратегического развития",
  "short_description": "Тестовое краткое описание подразделения.",
  "category": {
    "id": 1,
    "name": "Администрация",
    "slug": "administration"
  },
  "leader": {
    "full_name": "Руководитель 1",
    "photo": "https://<host>/media/departments/leaders/leader_photo_xxx.png",
    "position": "Руководитель отдела",
    "phone": "+99670000001",
    "email": "leader1@example.com",
    "address": "г. Чолпон-Ата, ул. Советская, 1"
  },
  "order": 1
}
```

`GET /api/departments/{id}/` - тот же формат одного объекта.

### Department categories
`GET /api/department-categories/`

Response item:
```json
{
  "id": 1,
  "name": "Администрация",
  "slug": "administration",
  "order": 1
}
```

`GET /api/department-categories/{id}/` - тот же формат одного объекта.

### Media
`GET /api/media/`  
Параметры: `category_id`, `type=photo|video`

Response item:
```json
{
  "id": 1,
  "type": "photo",
  "title": "Фото материал 1",
  "file": "https://<host>/media/media/items/media_photo_xxx.png",
  "preview_image": "https://<host>/media/media/previews/media_preview_xxx.png",
  "category": {
    "id": 1,
    "name": "Фотоотчеты",
    "slug": "photo-reports"
  },
  "order": 1,
  "created_at": "2026-02-28T10:00:00Z"
}
```

`GET /api/media/{id}/` - тот же формат одного объекта.

### Media categories
`GET /api/media-categories/`

Response item:
```json
{
  "id": 1,
  "name": "Фотоотчеты",
  "slug": "photo-reports",
  "order": 1
}
```

`GET /api/media-categories/{id}/` - тот же формат одного объекта.

## Admin endpoints (нужен Token)
- `GET|POST /api/admin/news/`
- `GET|PUT|PATCH|DELETE /api/admin/news/{id}/`
- `GET|POST /api/admin/news-categories/`
- `GET|PUT|PATCH|DELETE /api/admin/news-categories/{id}/`
- `GET|POST /api/admin/sights/`
- `GET|PUT|PATCH|DELETE /api/admin/sights/{id}/`
- `GET|POST /api/admin/sight-images/`
- `GET|PUT|PATCH|DELETE /api/admin/sight-images/{id}/`
- `GET|POST /api/admin/departments/`
- `GET|PUT|PATCH|DELETE /api/admin/departments/{id}/`
- `GET|POST /api/admin/department-categories/`
- `GET|PUT|PATCH|DELETE /api/admin/department-categories/{id}/`
- `GET|POST /api/admin/department-leaders/`
- `GET|PUT|PATCH|DELETE /api/admin/department-leaders/{id}/`
- `GET|POST /api/admin/media/`
- `GET|PUT|PATCH|DELETE /api/admin/media/{id}/`
- `GET|POST /api/admin/media-categories/`
- `GET|PUT|PATCH|DELETE /api/admin/media-categories/{id}/`
