from django.contrib import admin
from .models import Klins
# Register your models here.

class KlinsAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'data', 'flag', 'addtime']
    search_fields = ['name']
    list_filter = ['flag']
    list_per_page = 10

admin.site.register(Klins,KlinsAdmin)