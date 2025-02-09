from django.db import models

class Stock(models.Model):
    RATING_CHOICES = [
        ('A', 'Excellent'),
        ('B', 'Good'),
        ('C', 'Average'),
        ('D', 'Below Average'),
        ('E', 'Poor'),
    ]
    
    STRATEGY_CHOICES = [
        ('GROWTH', 'Growth'),
        ('VALUE', 'Value'),
        ('MOMENTUM', 'Momentum'),
        ('QUALITY', 'Quality'),
        ('DIVIDEND', 'Dividend'),
        ('CONTRARIAN', 'Contrarian'),
    ]
    
    
    country = models.CharField(max_length=10, default="US") 
    symbol = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    last_price = models.DecimalField(max_digits=10, decimal_places=2)
    ek_rating = models.CharField(max_length=1, choices=RATING_CHOICES)
    investment_strategy = models.CharField(max_length=20, choices=STRATEGY_CHOICES)
    
    # Fundamental Data
    market_cap = models.BigIntegerField()
    pe_ratio = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    eps_growth = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    dividend_yield = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    price_to_book = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    debt_to_equity = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    current_ratio = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    profit_margin = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    
    # Technical Data
    rsi = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    fifty_two_week_high = models.DecimalField(max_digits=10, decimal_places=2)
    fifty_two_week_low = models.DecimalField(max_digits=10, decimal_places=2)
    sma_50 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    sma_200 = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['symbol']

    def __str__(self):
        return f"{self.symbol} - {self.name}"