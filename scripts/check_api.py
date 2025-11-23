import requests, os, json

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stocktracker.settings")
import django

django.setup()
from django.conf import settings

url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=AAPL&interval=1min&apikey={settings.ALPHA_KEY}"
data = requests.get(url).json()
print(json.dumps(data.get("Meta Data", data), indent=2))