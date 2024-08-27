To run this project, please run step by step each command below, these commands will add data to database:
```
docker compose run --rm app sh -c "python manage.py migrate"
docker compose run --rm app sh -c "python manage.py add_movies"
docker compose run --rm app sh -c "python manage.py add_screenings ./data/showtimes.csv"
docker compose run --rm app sh -c "python manage.py add_ticket_types"
```
When running `docker compose run --rm app sh -c "python manage.py add_screenings ./data/showtimes.csv"` command please ignore `RuntimeWarning`

Then run:
```
docker compose up --build
```
`app/data/` contain data for database and index for semantic search.
`app/model_rm/`  contain recommendation model.
`app/movies/` contain movie-related functionality.
`app/user/` contain user-related functionality. 
`app/cart` contain shopping cart functionality.
`app/mysite/`: Django project settings and configurations.

