# Construct_Inc.

Repository with Construct site architecture for VKR. \
Python 3.9
---

## Requirements:
- DJANGO
  - django==4.1.4 (monolith framework)
  - django-ckeditor==6.5.1 (??? FOR NO USAGE)
  - djangorestframework==3.14 (Django rest framework)
  - django-filter==22.1
  - django-cors-headers==3.13 (for CORS)
  - djangorestframework-api-key==2.2 (Api auth)
  - WhiteNoise==2.0.6 (For testing locally with debug False FOR NO USAGE)
- DOCS
  - drf-yasg==1.21.4 (swagger)
  - pdocs3==0.10 (??? FOR NO USAGE)
  - sphinx==5.3 (documentation)
  - Pallets-Sphinx-Themes==2.0.3 (sphinx theme)
  - sphinx-rtd-theme==1.1.1 (sphinx theme)
  - myst-parser==0.18.1 (for sphinx interaction with md)
  - furo==2022.12.7 (sphinx theme)
- DB
  - mysqlclient==2.1.1 (for connecting to mysql db) (??? FOR NO USAGE)
  - psycopg2==2.9.6 (for connecting to postgres db)
- PYTHON
  - pillow==9.3 (images work)
  - loguru==0.6.0 (logging)
  - python-dotenv==0.21.0 (.env load)
  - markdown==3.4.1 (??? FOR NO USAGE)
- FastAPI
  - fastapi==0.89.1 (api development)
  - uvicorn==0.20.0 (fastapi running)
  - pydantic==1.10.4 (models)
  - sqlalchemy==2.0.0 (ORM)
- Bot
  - aiogram==2.25.1 (telegram)
- Sort
  - black==23.3.0 (code reformat by black profile)
  - isort==5.12.0 (imports reformatting)
- PDF
  - fpdf==1.7.2 (to geterate plate scheme)
  - aspose-pdf==23.4.0 (to geterate plate scheme) (FOR NO USAGE)
---
## Logs
- api_view_logs.log (API methods logs)
- server_logs.log (server work)
- orders_logs.log (logs for orders)
- logs.log
- bot_logs.log (in plans)
---
## Example of file config/secret.json
```json
{
  "PATH_LOG": "path_for_writing_logs",
  "HasAPIKey": "permission_api_key",
  "user_host": "sender_mail_address",
  "user_host_password": "sender_mail_address_password_for_localhost",
  "recipients_email": ["list_of_recipients_emails"],
  "TOKEN": "telegram_bot_secret_token"
}
```
---
## Example of file config/.env
```text
SECRET_KEY=django-secret_key
ALLOWED_HOSTS=allowed_hosts_list

DB_NAME=database_name
DB_USER=database_user
DB_HOST=database_host
DB_PASSWORD=database_password
DB_PORT=database_port

SERVER_HOST=fastapi_server_host
```
