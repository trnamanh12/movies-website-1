to run this project, please run step by step each command below:
```
docker compose run --rm app sh -c "python manage.py migrate"
docker compose run --rm app sh -c "python manage.py add_movies"
docker compose run --rm app sh -c "python manage.py add_screenings ./data/showtimes.csv"
docker compose run --rm app sh -c "python manage.py add_ticket_types"
docker compose up --build
```
Then go to localhost:80 (nginx) or localhost:8888 ( django )
when running `docker compose run --rm app sh -c "python manage.py add_screenings ./data/showtimes.csv"` command please ignore `RuntimeWarning`
