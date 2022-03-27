#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from os.path import exists, dirname, join

BASE_DIR = dirname(__file__)
env_file = join(dirname(BASE_DIR), "config.env")

if not exists(env_file):
    env_file = "D:Project/config.env"

if exists(env_file):
    with open(env_file, "r", encoding='utf-8') as config_file:
        config_item = config_file.readlines()
        for line in config_item:
            try:
                key, value = line.split("=")
            except:
                key, value = None, None
            if key and value:
                os.environ.update({key: value})


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'songs.settings')
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
