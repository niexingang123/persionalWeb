#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.contrib import admin
# from shares.models import Klins

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'persionalweb.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

    # admin.site.register(Klins)
    #
    # @admin.register(Klins)
    # class BlogAdmin(admin.ModelAdmin):
    #     search_fields = ('name')
    #     list_display=('id', 'code', 'name', 'data','addtime')

if __name__ == '__main__':
    main()
