# Generated by Django 5.0.1 on 2025-03-17 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_remove_ingredient_current_stock_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredientorder',
            name='section',
            field=models.CharField(choices=[('SANDWICH', 'Sandwich Section'), ('HOT', 'Hot Section'), ('COFFEE', 'Coffee Section'), ('GENERAL', 'General')], default='GENERAL', max_length=20),
        ),
    ]
