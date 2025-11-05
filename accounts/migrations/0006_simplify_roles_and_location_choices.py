from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_customuser_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(
                choices=[('ADMIN', 'Admin'), ('STAFF', 'Staff'), ('ORDERER', 'Orderer')],
                default='ORDERER',
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='location',
            field=models.CharField(
                blank=True,
                choices=[('180 Queen', '180 Queen'), ('151 Yonge', '151 Yonge'), ('33 Yonge', '33 Yonge')],
                help_text='Restaurant location',
                max_length=100,
            ),
        ),
    ]

