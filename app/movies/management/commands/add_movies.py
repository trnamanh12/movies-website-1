from django.core.management.base import BaseCommand
from movies.models import Movie
import csv
from datetime import datetime

class Command(BaseCommand):
    help = 'Add multiple movies to the Movie model'

    def read_movies_from_csv(self, file_path):
        movies = []
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row['vote_average'] = float(row['vote_average'])
                row['vote_count'] = int(row['vote_count'])
                row['release_date'] = datetime.strptime(row['release_date'], '%Y-%m-%d').date()
                row['revenue'] = float(row['revenue'])
                row['image'] = row.pop('poster_path')
                row['trailer'] = row.pop('youtubeId')
                movies.append(row)
        return movies

    def handle(self, *args, **kwargs):
        file_path = './data/movies1.csv' 
        movies = self.read_movies_from_csv(file_path)
        
        movie_objects = [Movie(**movie) for movie in movies]
        Movie.objects.bulk_create(movie_objects)

        self.stdout.write(self.style.SUCCESS('Successfully added movies to the database'))