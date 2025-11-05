from django.db import migrations


def create_default_stations(apps, schema_editor):
    Station = apps.get_model('orders', 'Station')
    defaults = [
        'Sandwich Station',
        'Salad Bar',
        'Hot Station',
        'Front Fridge',
    ]
    for name in defaults:
        Station.objects.get_or_create(name=name)


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_station_stationingredient'),
    ]

    operations = [
        migrations.RunPython(create_default_stations, migrations.RunPython.noop),
    ]

