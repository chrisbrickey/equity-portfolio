# stock-trading
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
Stock-trading is a single-page web application that utilizes a Django backend and *tbd* frontend.
- python x.x.x
- Django x.x.x
- Django Rest Framework x.x.x

*See requirements.txt and requirements-dev.txt for full list of dependencies.*


## Run the Program
- Open virtual environment: `. venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`
- Migrate the database: `./manage.py makemigrations` then `./manage.py migrate`
- Load data from seed: `./manage.py loaddata initdata.json`
- Run development server locally: `./manage.py runserver`


## Troubleshooting
- If static files are not running locally: `./manage.py collectstatic`
