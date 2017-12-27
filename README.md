# Stock Tracker
Xyzzzzzzzzzzzzzz


## Features Highlight

#### A
Xyzzzzzzzzzzzzzz

#### B
Xyzzzzzzzzzzzzzz


## Future Development

#### Up/Down Indicator
Alongside the last trade price show, user sees a green up arrow or red down arrow depending on whether it's gone up or down since the last quote

#### Currency Conversion
User can view values in currencies other than USD

#### Multiple Markets
User can access other securities markets


## Technology
Stock Tracker is a single-page web application that utilizes a Django backend and *tbd* frontend.
- python 2.7.10
- django 1.11 (latest version using python 2.7)
- django Rest Framework 3.7.7
- psycopg2 2.7.3.2 (package for working with Postgres)

*See requirements.txt and requirements-dev.txt for full list of dependencies.*


## Run the Program
- Open virtual environment: `. env/bin/activate`
- Install dependencies: `pip install -r requirements.txt`
- Migrate the database: `./manage.py makemigrations` then `./manage.py migrate`
- Load data from seed: `./manage.py loaddata initdata.json`
- Run development server locally: `./manage.py runserver`


## Troubleshooting
- If static files are not running locally: `./manage.py collectstatic`
