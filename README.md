to run this project:
```
docker compose run --rm app sh -c "python manage.py migrate"
docker compose run --rm app sh -c "python manage.py add_movies"
docker compose run --rm app sh -c "python manage.py add_screenings ./data/showtimes.csv"
docker compose up --build
```