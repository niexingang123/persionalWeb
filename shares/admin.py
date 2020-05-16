from django.contrib import admin
from .models import Klins,Stocks

class KlinsAdmin(admin.ModelAdmin):
    list_display = ['id','fid', 'code', 'name', 'short_data', 'flag', 'addtime']
    search_fields = ['name']
    list_filter = ['flag']
    list_per_page = 10
    ordering = ['id']
class StocksAdmin(admin.ModelAdmin):
    list_display = ['id','fid', 'code', 'name', 'industry', 'area', 'price_change', 'pricediff', 'totals', 'short_data', 'addtime']
    search_fields = ['name']
    list_per_page = 10
    ordering = ['id']
admin.site.register(Klins,KlinsAdmin)
admin.site.register(Stocks,StocksAdmin)