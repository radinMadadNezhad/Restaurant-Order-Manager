from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_contactmessage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='StationIngredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ingredient', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='station_links', to='orders.ingredient')),
                ('station', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='station_ingredients', to='orders.station')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='stationingredient',
            unique_together={('station', 'ingredient')},
        ),
    ]

