# Generated by Django 3.2.8 on 2021-11-22 11:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('like_users', models.ManyToManyField(related_name='like_collections', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Form',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_id', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=200)),
                ('overview', models.TextField(blank=True)),
                ('poster_path', models.CharField(blank=True, max_length=300)),
                ('release_date', models.DateField(blank=True)),
                ('hits', models.PositiveIntegerField(default=0)),
                ('vote_average', models.FloatField(default=0)),
                ('vote_count', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('api_id', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=200)),
                ('overview', models.TextField(blank=True)),
                ('poster_path', models.CharField(blank=True, max_length=300)),
                ('release_date', models.DateField(blank=True)),
                ('hits', models.PositiveIntegerField(default=0)),
                ('vote_average', models.FloatField(default=0)),
                ('vote_count', models.PositiveIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('like_users', models.ManyToManyField(related_name='like_movies', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=50)),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='movies.collection')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('like_users', models.ManyToManyField(related_name='like_movie_reviews', to=settings.AUTH_USER_MODEL)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='movies.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='wrtie_reviews', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='collection',
            name='movies',
            field=models.ManyToManyField(related_name='collections', to='movies.Movie'),
        ),
        migrations.AddField(
            model_name='collection',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_collections', to=settings.AUTH_USER_MODEL),
        ),
    ]
