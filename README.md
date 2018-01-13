# Equity Portfolio
Equity Portfolio is a single-page web application that utilizes a Django for both front and back end as well as Django Rest Framework to provide a browsable API.


## Features Highlight

#### Browsable API
Non-technical users may interact only with the templates, but a hyperlinked, browsable API is also available using the /api path.

#### Navigation
Buttons in the footer help users navigate the site's functionality.


## Technology
*See requirements.txt for full list of dependencies.*
- Python 2.7.10
- Django 1.11 (latest version using python 2.7)
- Django Rest Framework 3.7.7


## Run the Program
1. Add your own AlphaVantage API key
  - Get an AlphaVantage API key [here](https://www.alphavantage.co/).
  - Add that string to your local environment variables, e.g. `ALPHA_KEY="copy/paste your key here"`.
2. Enter the virtual environment
  - `. env/bin/activate`
3. Install dependencies
  - `pip install -r requirements.txt`
4. Migrate the database
  - `./manage.py makemigrations` then `./manage.py migrate`
5. Load data from seed
  - `./manage.py loaddata initdata.json`
6. Run development server locally
  - `./manage.py runserver`


## Future Development
- Live Update: Portfolio updates every 5 seconds
- Up/Down Indicator: Alongside the last trade price show, user sees a green up arrow or red down arrow depending on whether it's gone up or down since the last quote
- Multiple Portfolios: Users can own multiple portfolios
- Authentication: System can handle multiple users and provide reasonable level of security
- Currency Conversion: User can view values in currencies other than USD
