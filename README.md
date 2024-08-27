to run this project, please run step by step each command below, these commands will add data to database:
```
docker compose run --rm app sh -c "python manage.py migrate"
docker compose run --rm app sh -c "python manage.py add_movies"
docker compose run --rm app sh -c "python manage.py add_screenings ./data/showtimes.csv"
docker compose run --rm app sh -c "python manage.py add_ticket_types"
```
Then
```
docker compose up --build
```
when running `docker compose run --rm app sh -c "python manage.py add_screenings ./data/showtimes.csv"` command please ignore `RuntimeWarning`
