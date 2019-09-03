from django.contrib import admin

# Register your models here.
from django.utils.translation import ugettext_lazy as _

from .models import Currency, ExchangeTrades


class BaseAdmin(admin.ModelAdmin):
    save_on_top = True


class CurrencyAdmin(BaseAdmin):
    list_display = ('code', 'name',)
    list_filter = ['code', 'name']
    search_fields = ('code', 'name',)
    list_editable = ('name',)


class ExchangeTradesAdmin(BaseAdmin):
    readonly_fields = ('identifier', )
    list_display = ('sell_currency', 'sell_amount', 'buy_currency', 'buy_amount', 'rate', 'date_booked')
    list_filter = ['sell_currency', 'sell_amount', 'buy_currency', 'buy_amount', 'rate', 'date_booked']
    search_fields = ('sell_currency', 'sell_amount', 'buy_currency', 'buy_amount', 'rate', 'date_booked')
    ordering = ('-date_booked',)




admin.site.register(Currency, CurrencyAdmin)
admin.site.register(ExchangeTrades, ExchangeTradesAdmin)
