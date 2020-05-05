from django.contrib import admin
from .models import Klins
# Register your models here.

class KlinsAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name', 'short_data', 'flag', 'addtime']
    search_fields = ['name']
    list_filter = ['flag']
    list_per_page = 10
    ordering = ['id']

admin.site.register(Klins,KlinsAdmin)