# Generated by Django 5.1.4 on 2025-02-20 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0007_booking_user_email_alter_booking_movie_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='theater',
            name='price',
            field=models.DecimalField(decimal_places=2, default=250.0, max_digits=10),
        ),
    ]
