# Equity Portfolio
[www.equity-portfolio.com](https://www.equity-portfolio.com/) allows users to search for equities across multiple markets and include them in their portfolio with amount of shares owned.  The portfolio updates so users can view the current value of each investment.  This app utilizes Django for both front and back end as well as Django Rest Framework to provide a browsable API.


## Features Highlight

#### 3rd party data service
This app utilizes AlphaVantage API to retrieve information on stocks in the portfolio and new stocks via search.

#### Browsable API
Non-technical users may interact only with HTML templates, but a hyperlinked, browsable API is also available using the /api namespace.


## Technology
*See requirements.txt for full list of dependencies.*
- Python 2.7.10
- Django 1.11
- Django Rest Framework 3.7.7


## Run the Program
1. Add your own AlphaVantage API key
  - Get an AlphaVantage API key [here](https://www.alphavantage.co/).
  - Add that string to your local environment variables, e.g. `export ALPHA_KEY="copy/paste your key here"`.
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
- Multiple Portfolios: Users can own multiple portfolios
- Live Update: Portfolio updates every 5 seconds without redirect or reload.
- Authentication: System can handle multiple users and provide reasonable level of security
- Currency Conversion: User can view values in currencies other than USD
- Up/Down Indicator: Alongside the last trade price show, user sees a green up arrow or red down arrow depending on whether it's gone up or down since the last quote
