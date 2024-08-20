# Generated by Django 5.0.7 on 2024-08-20 16:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0008_alter_movie_revenue_alter_movie_vote_average'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_watched', models.DateTimeField(auto_now=True)),
                ('saved', models.BooleanField(default=False)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_histories', to='movies.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'User Histories',
                'unique_together': {('user', 'movie')},
            },
        ),
    ]