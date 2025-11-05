from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0013_seed_default_stations'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredientorder',
            name='location',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='ingredientorder',
            name='station',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.deletion.SET_NULL, related_name='orders', to='orders.station'),
        ),
    ]

