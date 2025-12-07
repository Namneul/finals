#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import pymysql


"""def create_database_if_not_exists():
    DB_NAME = "finals"
    DB_USER = "root"
    DB_PASSWORD = "123123"
    DB_HOST = "localhost"

    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            charset='utf8mb4',
        )
        conn.autocommit(True)

        with conn.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")

        conn.close()
        print("Database `{DB_NAME}` created")
    except Exception as e:
        print(f"Database `{DB_NAME}` could not be created: {e}")
        sys.exit(1)
        """


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'final_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
