# Generated by Django 3.2.7 on 2021-09-14 06:38

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Film',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='UUID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('plot', models.TextField(blank=True, verbose_name='Описание')),
                ('creation_date', models.DateField(blank=True, verbose_name='Год выпуска')),
                ('certificate', models.TextField(blank=True, verbose_name='Сертификат')),
                ('file_path', models.FileField(blank=True, upload_to='films/', verbose_name='Файл')),
                ('rating', models.FloatField(blank=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)], verbose_name='Рейтинг')),
                ('type', models.CharField(choices=[('movie', 'Фильм'), ('series', 'Сериал')], default='movie', max_length=7, verbose_name='Тип')),
            ],
            options={
                'verbose_name': 'Кинопроизведение',
                'verbose_name_plural': 'Кинопроизведения',
                'db_table': 'movies',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='UUID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Жанр',
                'verbose_name_plural': 'Жанры',
                'db_table': 'genres',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='UUID')),
                ('name', models.CharField(max_length=127, verbose_name='Имя')),
            ],
            options={
                'verbose_name': 'Персона',
                'verbose_name_plural': 'Персоны',
                'db_table': 'persons',
            },
        ),
        migrations.CreateModel(
            name='PersonsFilms',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='UUID')),
                ('part', models.CharField(choices=[('a', 'Актер'), ('w', 'Сценарист'), ('d', 'Режиссер')], max_length=1, verbose_name='Роль')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.film')),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.person')),
            ],
            options={
                'db_table': 'persons_movies',
            },
        ),
        migrations.AddField(
            model_name='person',
            name='films',
            field=models.ManyToManyField(through='main_app.PersonsFilms', to='main_app.Film', verbose_name='Фильмы'),
        ),
        migrations.CreateModel(
            name='GenresFilms',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='UUID')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.genre')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.film')),
            ],
            options={
                'db_table': 'genres_movies',
            },
        ),
        migrations.AddField(
            model_name='film',
            name='genre_set',
            field=models.ManyToManyField(blank=True, through='main_app.GenresFilms', to='main_app.Genre'),
        ),
    ]
