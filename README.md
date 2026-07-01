# Equity Portfolio
Users search for equities across multiple markets and include them in their portfolio with amount of shares owned.  
The portfolio updates so users can view the current value of each investment.  
Equity Portfolio utilizes Django for both front and back end as well as Django Rest Framework to provide a browsable API.

_This app was previously hosted at www.equity-portfolio.com._

## Features Highlight

#### 3rd party data service
This app utilizes AlphaVantage API to retrieve information on stocks in the portfolio and new stocks via search.

#### Browsable API
Non-technical users may interact via the browser with HTML templates, but a hyperlinked, browsable API is also available using the /api namespace.


## Tech Stack
*See requirements.txt for full list of dependencies.*
- Python 3.12
- Django 3.2 LTS
- Django Rest Framework 3.14
- PostgreSQL


## Environment Variables
This application uses environment variables for configuration.
- `ALPHA_KEY`: AlphaVantage API key for stock price data
- `SECRET_KEY`: Django secret key for cryptographic signing
- `DATABASE_URL`: PostgreSQL database connection string

In production environments, these variables must be explicitly set using real values. (Heroku automatically sets `DATABASE_URL`.)
For local development, default values are provided with the exception of `ALPHA_KEY`. 
You must obtain a free AlphaVantage API key and set that variable using the instructions below.

### Setting environment variables for local development

1. Create a `.env` file.
- Create a file called `.env` at the top level of the repo. 
- This file is gitignored to prevent committing secrets.
- Copy the content of `.env.example` (committed in this repo) into your new file.

2. Set `ALPHA_KEY`.
- Get a free API key at [AlphaVantage](https://www.alphavantage.co/support/#api-key)
- Replace `your_alphavantage_api_key_here` in `.env` with the actual API key.

_To run the app locally, the above are the only required steps with regard to environment variables._

3. (optional) Set `SECRET_KEY`.
- Some value must be defined for this variable in order for Django to start. But you don't need a real cryptographic key
if you are only handling test/seed data on a local server. So the `.env` file already contains an obviously insecure 
default string that you can use for local development: `SECRET_KEY=django-insecure-local-dev-key-change-in-production`.
- If you want to use a real cryptographic key or local development, replace `django-insecure...` with that key in `.env`.
- Never use the insecure default string in production.

4. (optional) Set `DATABASE_URL`.
- This PostgreSQL configuration is currently defined in settings.py, but it can be overridden by defining `DATABASE_URL` in `.env`.
- This environment variable is automatically set by Heroku in production.

#### Alternative: Store environment variables in terminal shell
```
export ALPHA_KEY="your-api-key-here" # required for local development
export SECRET_KEY="your-secret-key-here" # optional for local development
```
_NB: These terminal exports are temporary and only persist for the current terminal session._


## Run the Program
The below will not work if the Alpha Vantage API key is not set as an environment variable (see previous section).

### 1. Install and and Start PostgreSQL

**macOS (using Homebrew):**
```bash
# Install PostgreSQL
brew install postgresql@14

# Start PostgreSQL service (auto-starts on boot)
brew services start postgresql@14

# Create the database
createdb stocktracker_dev1

# Verify database was created
psql -l | grep stocktracker
```

**Alternative: Start PostgreSQL temporarily** (stops when terminal closes)
```bash
pg_ctl -D /opt/homebrew/var/postgresql@14 start
```

### 2. Create Python Virtual Environment
```bash
# Create virtual environment with Python 3.12
uv venv --python 3.12

# Activate it
source .venv/bin/activate
```

### 3. Install Python Dependencies
```bash
uv pip install -r requirements.txt
```

### 4. Run Database Migrations
```bash
python manage.py migrate
```

### 5. Load Seed Data
```bash
python manage.py loaddata tracker_app/fixtures/initdata.json
```

### 6. Start Development Server
```bash
python manage.py runserver
```
_In production, the server will be initiated via stocktracker/wsgi.py._

### 7. View the Web Application
Open http://localhost:8000 in your browser


## More on Local Development

### Run Test Suite
```
python manage.py test -v 3
```

### Manage Seed Data
Database seed data is defined by `tracker_app/fixtures/initdata.json`. 
The current seeds include a portfolio with the below equities.

     | Stock  | Ticker | Shares | Price   | 
     |--------|--------|--------|---------|
     | Apple  | AAPL   | 20     | $228.52 | 
     | Nvidia | NVDA   | 15     | $140.11 | 
     | Google | GOOGL  | 10     | $169.24 | 

You can change the seeding by updating `initdata.json` and then flushing the database and reloading the seed data.

### Flush local database
```
# Clear all data from the database
python manage.py flush --no-input

# Reload the seed data
python manage.py loaddata tracker_app/fixtures/initdata.json
```

### Check AlphaVantage API
```
# runs script  
python scripts/check_api.py
```


## Future Development
- Multiple Portfolios: Users can own multiple portfolios
- Live Update: Portfolio updates every 5 seconds without redirect or reload.
- Authentication: System can handle multiple users and provide reasonable level of security
- Currency Conversion: User can view values in currencies other than USD
- Up/Down Indicator: Alongside the last trade price show, user sees a green up arrow or red down arrow depending on whether it's gone up or down since the last quote
