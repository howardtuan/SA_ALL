# Generated by Django 4.1.4 on 2022-12-31 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0014_exchange_date_history_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='exchange',
            name='ITEM_NAME',
            field=models.CharField(default=int, max_length=20),
            preserve_default=False,
        ),
    ]
