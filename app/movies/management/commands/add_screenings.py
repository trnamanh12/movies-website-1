import csv
from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime
from movies.models import Movie, Cinema, Screening  

class Command(BaseCommand):
    help = 'Populate the database with screening data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file containing screening data')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']

        try:
            with open(csv_file, mode='r') as file:
                reader = csv.DictReader(file)

                for row in reader:
                    movie_title = row['movie_title']
                    cinema_name = row['cinema_name']
                    date_time_str = row['date_time']
                    
                    # Parse datetime
                    date_time = parse_datetime(date_time_str)
                    if date_time is None:
                        self.stdout.write(self.style.ERROR(f"Invalid date format: {date_time_str}"))
                        continue

                    # Get or create the Movie object
                    movie, created = Movie.objects.get_or_create(title=movie_title)
                    
                    # Get or create the Cinema object
                    cinema, created = Cinema.objects.get_or_create(name=cinema_name)
                    
                    # Create the Screening object
                    Screening.objects.create(
                        movie=movie,
                        cinema=cinema,
                        date_time=date_time
                    )

            self.stdout.write(self.style.SUCCESS('Successfully populated the database with screenings from CSV.'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File not found: {csv_file}"))
        except csv.Error as e:
            self.stdout.write(self.style.ERROR(f"CSV error: {e}"))