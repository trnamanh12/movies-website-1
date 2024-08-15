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
                # Correct data types
                row['vote_average'] = float(row['vote_average'])
                row['vote_count'] = int(row['vote_count'])
                row['release_date'] = datetime.strptime(row['release_date'], '%Y-%m-%d').date()
                row['revenue'] = float(row['revenue'])
                # Map poster_path to image
                row['image'] = row.pop('poster_path')
                movies.append(row)
        return movies

    def handle(self, *args, **kwargs):
        file_path = './data/out_cleaned1.csv'  # Path to your CSV file
        movies = self.read_movies_from_csv(file_path)
        
        movie_objects = [Movie(**movie) for movie in movies]
        Movie.objects.bulk_create(movie_objects)

        self.stdout.write(self.style.SUCCESS('Successfully added movies to the database'))