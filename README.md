# Stock Market Dashboard

A Django-based web application that provides real-time stock market data and analysis using the Yahoo Finance API.

## Features

- Real-time stock data from S&P 500 companies
- Interactive stock charts using Plotly
- Company information and fundamentals
- Technical analysis indicators
- Historical price data visualization

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Start the development server:
```bash
python manage.py runserver
```

5. Visit http://localhost:8000 in your browser

## Technology Stack

- Backend: Django
- Data Processing: yfinance, pandas
- Charts: Plotly
- Frontend: Bootstrap

## Project Structure

- `stockdashboard/` - Main Django project directory
- `stocks/` - Django app for stock-related functionality
- `templates/` - HTML templates
- `static/` - CSS, JavaScript, and other static files
