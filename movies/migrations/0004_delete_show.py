# Generated by Django 5.1.4 on 2025-02-09 08:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_show_delete_show_seats'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Show',
        ),
    ]
