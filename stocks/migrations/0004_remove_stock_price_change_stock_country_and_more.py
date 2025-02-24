# Generated by Django 5.1.1 on 2025-02-08 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0003_stock_price_change'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='price_change',
        ),
        migrations.AddField(
            model_name='stock',
            name='country',
            field=models.CharField(default='US', max_length=10),
        ),
        migrations.AlterField(
            model_name='stock',
            name='current_ratio',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='debt_to_equity',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='dividend_yield',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='ek_rating',
            field=models.CharField(choices=[('A', 'Excellent'), ('B', 'Good'), ('C', 'Average'), ('D', 'Below Average'), ('E', 'Poor')], max_length=1),
        ),
        migrations.AlterField(
            model_name='stock',
            name='eps_growth',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='fifty_two_week_high',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='stock',
            name='fifty_two_week_low',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='stock',
            name='investment_strategy',
            field=models.CharField(choices=[('GROWTH', 'Growth'), ('VALUE', 'Value'), ('MOMENTUM', 'Momentum'), ('QUALITY', 'Quality'), ('DIVIDEND', 'Dividend'), ('CONTRARIAN', 'Contrarian')], max_length=20),
        ),
        migrations.AlterField(
            model_name='stock',
            name='last_price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='stock',
            name='market_cap',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='stock',
            name='pe_ratio',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='price_to_book',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='profit_margin',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='rsi',
            field=models.DecimalField(decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='sma_200',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='stock',
            name='sma_50',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
