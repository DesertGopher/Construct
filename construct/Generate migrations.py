import os
from pathlib import Path
from django.core import management

DJANGO_SETTINGS = 'construct.settings'


def main():
    """ Метод для запуска миграции и записи в бд """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', DJANGO_SETTINGS)
    management.execute_from_command_line(['manage.py', 'makemigrations'])
    management.execute_from_command_line(['manage.py', 'migrate'])


if __name__ == "__main__":
    main()
