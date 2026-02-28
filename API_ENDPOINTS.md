# API endpoints

Base URL: `/api/`

## Auth
- `POST /api/auth/token/` - получить auth token

## Public endpoints
- `GET /api/news/`
- `GET /api/news/{id}/`
- `GET /api/news-categories/`
- `GET /api/news-categories/{id}/`
- `GET /api/sights/`
- `GET /api/sights/{id}/`
- `GET /api/departments/`
- `GET /api/departments/{id}/`
- `GET /api/department-categories/`
- `GET /api/department-categories/{id}/`
- `GET /api/media/`
- `GET /api/media/{id}/`
- `GET /api/media-categories/`
- `GET /api/media-categories/{id}/`

## Admin endpoints (требуют аутентификацию)
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
