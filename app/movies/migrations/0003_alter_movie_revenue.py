# Generated by Django 5.0.7 on 2024-08-15 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_remove_movie_description_remove_movie_rating_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='revenue',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=15),
        ),
    ]
