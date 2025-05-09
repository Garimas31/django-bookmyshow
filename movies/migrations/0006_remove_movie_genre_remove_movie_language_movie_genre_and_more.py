# Generated by Django 5.1.4 on 2025-02-09 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_genre_language_movie_genre_movie_language'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='genre',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='language',
        ),
        migrations.AddField(
            model_name='movie',
            name='genre',
            field=models.CharField(choices=[('action', 'Action'), ('comedy', 'Comedy'), ('drama', 'Drama')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='language',
            field=models.CharField(choices=[('hindi', 'Hindi'), ('english', 'English'), ('french', 'French')], max_length=20, null=True),
        ),
    ]
