# Generated by Django 4.1.4 on 2022-12-29 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_remove_exchange_item_id_exchange_item_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exchange_item',
            name='ID',
        ),
        migrations.AddField(
            model_name='exchange_item',
            name='id',
            field=models.BigAutoField(auto_created=True, default=int, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
