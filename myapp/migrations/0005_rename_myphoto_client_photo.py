# Generated by Django 4.1.3 on 2023-01-08 13:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0004_rename_photo_client_myphoto"),
    ]

    operations = [
        migrations.RenameField(
            model_name="client",
            old_name="MYPHOTO",
            new_name="PHOTO",
        ),
    ]
