#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

import cx_Oracle
cx_Oracle.init_oracle_client(lib_dir="LD_LIBRARY_PATH")
# cx_Oracle.init_oracle_client(lib_dir="./instantclient_19_8")


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comment_book.settings')
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
