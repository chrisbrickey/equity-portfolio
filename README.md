# Equity Portfolio
[www.equity-portfolio.com](https://www.equity-portfolio.com/) allows users to search for equities across multiple markets and include them in their portfolio with amount of shares owned.  The portfolio updates so users can view the current value of each investment.  This app utilizes Django for both front and back end as well as Django Rest Framework to provide a browsable API.


## Features Highlight

#### 3rd party data service
This app utilizes AlphaVantage API to retrieve information on stocks in the portfolio and new stocks via search.

#### Browsable API
Non-technical users may interact only with HTML templates, but a hyperlinked, browsable API is also available using the /api namespace.


## Technology
*See requirements.txt for full list of dependencies.*
- Python 3.12
- Django 3.2 LTS
- Django Rest Framework 3.14
- PostgreSQL


## Environment Variables

This application uses environment variables for configuration. For **local development**, the app will run with default values. For **production deployment** (Heroku), you must set these variables.

### Required for Production
- `SECRET_KEY` - Django secret key for cryptographic signing
- `ALPHA_KEY` - AlphaVantage API key for stock price data
- `DATABASE_URL` - PostgreSQL database connection string (automatically set by Heroku)

### Local Development
The app includes development defaults, so you can run locally without setting any environment variables. However, you'll need a real AlphaVantage API key for some features:

1. Get a free API key at [AlphaVantage](https://www.alphavantage.co/)
2. Set it in your terminal session:
   ```bash
   export ALPHA_KEY="your-api-key-here"
   ```

To set a custom SECRET_KEY for local testing:
```bash
export SECRET_KEY="your-secret-key-here"
```

**Note:** These exports are temporary and only last for your current terminal session. For permanent local configuration, add them to your shell profile (`~/.zshrc` or `~/.bashrc`).


## Run the Program

### 1. Install and Configure PostgreSQL

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

### 7. View the Web Application
Open http://localhost:8000 in your browser


## Future Development
- Multiple Portfolios: Users can own multiple portfolios
- Live Update: Portfolio updates every 5 seconds without redirect or reload.
- Authentication: System can handle multiple users and provide reasonable level of security
- Currency Conversion: User can view values in currencies other than USD
- Up/Down Indicator: Alongside the last trade price show, user sees a green up arrow or red down arrow depending on whether it's gone up or down since the last quote
