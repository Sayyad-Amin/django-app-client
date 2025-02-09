from django.contrib import admin
from .models import Stock

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = (
        'symbol', 
        'name', 
        'last_price', 
        'ek_rating', 
        'investment_strategy',
        'market_cap',
        'pe_ratio',
        'eps_growth',
        'dividend_yield',
        'rsi'
    )
    list_filter = (
        'ek_rating',
        'investment_strategy'
    )
    search_fields = (
        'symbol',
        'name'
    )
    readonly_fields = ('last_updated',)
    ordering = ('symbol',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('symbol', 'name', 'last_price', 'ek_rating', 'investment_strategy')
        }),
        ('Fundamental Data', {
            'fields': (
                'market_cap', 'pe_ratio', 'eps_growth', 'dividend_yield',
                'price_to_book', 'debt_to_equity', 'current_ratio', 'profit_margin'
            )
        }),
        ('Technical Data', {
            'fields': (
                'rsi', 'fifty_two_week_high', 'fifty_two_week_low',
                'sma_50', 'sma_200'
            )
        }),
        ('Metadata', {
            'fields': ('last_updated',)
        })
    )