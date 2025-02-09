# Generated by Django 5.1.1 on 2025-02-08 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0002_stock_current_ratio_stock_debt_to_equity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='price_change',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
