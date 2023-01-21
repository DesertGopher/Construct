# Construct_Inc.

Repository with Construct site architecture for VKR. \
Python 3.9
---

## Requirements:
- markdown==3.4.1 (??? for no usage now)
- django==4.1.4 (monolith framework)
- django-ckeditor==6.5.1 (??? for no usage now)
- pillow==9.3 (images work)
- djangorestframework==3.14 (Django rest framework)
- pdocs3==0.10 (??? for no usage now)
- sphinx==5.3 (documentation)
- Pallets-Sphinx-Themes==2.0.3 (sphinx theme)
- sphinx-rtd-theme==1.1.1 (sphinx theme)
- myst-parser==0.18.1 (for sphinx interaction with md)
- furo==2022.12.7 (sphinx theme)
- drf-yasg==1.21.4 (swagger)
- django-filter==22.1
- django-cors-headers==3.13 (for CORS)
- djangorestframework-api-key==2.2 (Api auth)
- loguru==0.6.0 (logging)
- WhiteNoise==2.0.6 (For testing locally with debug False)
- python-dotenv==0.21.0 (.env load)
- mysqlclient==2.1.1 (for connecting to mysql db)

---
## Logs
- api_view_logs.txt (API methods logs)

---
## Example of file config/secret.json
```json
{
  "PATH_LOG": "path_for_writing_logs",
  "HasAPIKey": "permission_api_key",
  "user_host": "sender_mail_address",
  "user_host_password": "sender_mail_address_password_for_localhost",
  "recipients_email": ["list_of_recipients_emails"]
}
```
---
## Example of file dotenv
```text
SECRET_KEY=django-secret_key
ALLOWED_HOSTS=allowed_hosts_list

DB_NAME=mysql_database_name
DB_USER=mysql_database_user
DB_HOST=mysql_database_host
DB_PASSWORD=mysql_database_password
DB_PORT=mysql_database_port
```