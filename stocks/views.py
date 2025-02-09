from django.shortcuts import render
from django.http import JsonResponse
import yfinance as yf
import pandas as pd
import numpy as np
from .models import Stock
from django.db.models import Q
import time
import requests

def fetch_stock_data(symbol, retries=3):
    """Fetch stock data from yfinance with error handling and retries"""
    for attempt in range(retries):
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            if 'currentPrice' not in info:
                print(f"No data found for {symbol}, possibly delisted.")
                return None
            hist = stock.history(period="1y")
            
            return {
                'symbol': symbol,
                'name': info.get('longName', ''),
                'last_price': info.get('currentPrice', 0) * 3.75,  # Convert USD to SAR
                'market_cap': info.get('marketCap', 0) * 3.75,  # Convert USD to SAR
                'pe_ratio': info.get('forwardPE', None),
                'eps_growth': info.get('earningsGrowth', None),
                'dividend_yield': info.get('dividendYield', None),
                'rsi': calculate_rsi(hist['Close']) if not hist.empty else None,
                'country': 'SA' if '.SR' in symbol else 'PK' if '.KAR' in symbol else 'US'
            }
        except requests.exceptions.ConnectionError:
            print(f"Connection error while fetching {symbol}. Retrying ({attempt+1}/{retries})...")
            time.sleep(5)
        except Exception as e:
            print(f"Error fetching data for {symbol}: {str(e)}")
            return None
    print(f"Failed to fetch data for {symbol} after {retries} retries.")
    return None


def calculate_rsi(prices, periods=14):
    """Calculate RSI technical indicator"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs)).iloc[-1]

def calculate_ek_rating(stock_data):
    """Calculate EK Global rating with enhanced criteria"""
    score = 0
    
    # Fundamental Factors (40%)
    if stock_data.get('pe_ratio'):
        if stock_data['pe_ratio'] < 12: score += 3
        elif stock_data['pe_ratio'] < 18: score += 2
        elif stock_data['pe_ratio'] < 25: score += 1
        
    if stock_data.get('debt_to_equity'):
        if stock_data['debt_to_equity'] < 0.3: score += 3
        elif stock_data['debt_to_equity'] < 0.7: score += 2
        elif stock_data['debt_to_equity'] < 1: score += 1

    # Technical Factors (30%)
    if stock_data.get('rsi'):
        if 40 < stock_data['rsi'] < 60: score += 2  # Neutral zone
        elif 30 < stock_data['rsi'] < 70: score += 1
        
    if stock_data.get('sma_50') and stock_data.get('sma_200'):
        if stock_data['sma_50'] > stock_data['sma_200']: score += 1

    # Growth Factors (30%)
    if stock_data.get('eps_growth'):
        if stock_data['eps_growth'] > 0.2: score += 3
        elif stock_data['eps_growth'] > 0.1: score += 2
        elif stock_data['eps_growth'] > 0.05: score += 1

    # Country Adjustment (From Excel allocations)
    if stock_data.get('country') == 'SA':  # Saudi Arabia
        score += 1
    elif stock_data.get('country') == 'PK':  # Pakistan
        score += 0.5

    # Normalize to A-E scale
    if score >= 9: return 'A'
    elif score >= 7: return 'B'
    elif score >= 5: return 'C' 
    elif score >= 3: return 'D'
    else: return 'E'

def determine_strategy(stock_data):
    """Determine the best investment strategy for the stock"""
    strategies = []
    
    # Growth Strategy
    if (stock_data.get('eps_growth', 0) or 0) > 0.15:
        strategies.append('GROWTH')
    
    # Value Strategy
    if (stock_data.get('pe_ratio', float('inf')) or float('inf')) < 15:
        strategies.append('VALUE')
    
    # Momentum Strategy
    if stock_data.get('rsi', 0) > 50:
        strategies.append('MOMENTUM')
    
    # Quality Strategy
    if ((stock_data.get('debt_to_equity', float('inf')) or float('inf')) < 1 and 
        (stock_data.get('profit_margin', 0) or 0) > 0.15):
        strategies.append('QUALITY')
    
    # Dividend Strategy
    if (stock_data.get('dividend_yield', 0) or 0) > 0.03:
        strategies.append('DIVIDEND')
    
    return strategies[0] if strategies else 'GROWTH'  # Default to GROWTH if no clear strategy

def update_stock_database():
    """Update stock database with latest data for specified Saudi companies"""
    saudi_symbols = [
        '4070.SR', '4071.SR', '4072.SR', '4210.SR', '7010.SR', '7020.SR', '7030.SR', '7040.SR',
        # ... (rest of the symbols)
    ]

    for symbol in saudi_symbols:
        stock_data = fetch_stock_data(symbol)
        if stock_data:
            stock_data['ek_rating'] = calculate_ek_rating(stock_data)
            stock_data['investment_strategy'] = determine_strategy(stock_data)
            
            Stock.objects.update_or_create(
                symbol=stock_data['symbol'],
                defaults=stock_data
            )
        else:
            print(f"Skipping {symbol} due to missing data.")

def dashboard(request):
    """Render the main dashboard view"""
    update_stock_database()
    
    context = {
        'default_filters': {
            'ratings': ['A', 'B', 'C', 'D', 'E'],
            'strategies': ['GROWTH', 'VALUE', 'MOMENTUM', 'QUALITY', 'DIVIDEND'],
            'legends': ['buffett', 'lynch', 'graham'],
            'popular_filters': ['low_pe', 'high_dividend', 'strong_growth', 'below_book', 'oversold']
        }
    }
    return render(request, 'stocks/dashboard.html', context)

def screener(request):
    """Handle stock screener requests with customizable filters"""
    
    # Retrieve filters from GET parameters
    rating = request.GET.get('rating')
    strategy = request.GET.get('strategy')
    legend = request.GET.get('legend')
    smart_pick = request.GET.get('smart_pick') == 'true'
    filter_type = request.GET.get('filter')
    country = request.GET.get('country')

    stocks = Stock.objects.all()

    # Apply filters based on user input
    if rating:
        stocks = stocks.filter(ek_rating=rating)
    if strategy:
        stocks = stocks.filter(investment_strategy=strategy)
    if legend:
        stocks = apply_legend_criteria(stocks, legend)
    if smart_pick:
        stocks = smart_picks(stocks)
    if filter_type:
        stocks = apply_popular_filters(stocks, filter_type)
    if country and country != 'ALL':
        stocks = stocks.filter(country=country)

    # Prepare stock data for response
    stock_data = []
    for stock in stocks:
        stock_data.append({
            'symbol': stock.symbol,
            'name': stock.name,
            'last_price': float(stock.last_price),
            'market_cap': stock.market_cap,
            'pe_ratio': float(stock.pe_ratio) if stock.pe_ratio else None,
            'eps_growth': float(stock.eps_growth) if stock.eps_growth else None,
            'dividend_yield': float(stock.dividend_yield) if stock.dividend_yield else None,
            'rsi': float(stock.rsi) if stock.rsi else None,
            'ek_rating': stock.ek_rating,
            'strategy': stock.investment_strategy,
            'price_to_book': float(stock.price_to_book) if stock.price_to_book else None,
            'debt_to_equity': float(stock.debt_to_equity) if stock.debt_to_equity else None,
            'current_ratio': float(stock.current_ratio) if stock.current_ratio else None,
            'profit_margin': float(stock.profit_margin) if stock.profit_margin else None,
            'fifty_two_week_high': float(stock.fifty_two_week_high) if stock.fifty_two_week_high else None,
            'fifty_two_week_low': float(stock.fifty_two_week_low) if stock.fifty_two_week_low else None,
            'sma_50': float(stock.sma_50) if stock.sma_50 else None,
            'sma_200': float(stock.sma_200) if stock.sma_200 else None
        })

    return JsonResponse({'status': 'success', 'data': stock_data})

def apply_legend_criteria(stocks, legend):
    """Apply investment legend criteria"""
    if legend == 'buffett':
        return stocks.filter(
            pe_ratio__lt=15,
            debt_to_equity__lt=0.5,
            profit_margin__gt=0.2,
            current_ratio__gt=1.5
        )
    elif legend == 'lynch':
        return stocks.filter(
            pe_ratio__lt=15,
            eps_growth__gt=0.15
        )
    elif legend == 'graham':
        return stocks.filter(
            price_to_book__lt=1.5,
            current_ratio__gt=2,
            debt_to_equity__lt=1
        )
    return stocks

def smart_picks(stocks):
    """Apply smart picks criteria"""
    return stocks.filter(
        ek_rating__in=['A', 'B'],
        pe_ratio__lt=20,
        eps_growth__gt=0,
        rsi__gt=30,
        rsi__lt=70
    )

def apply_popular_filters(stocks, filter_type):
    """Apply popular filter criteria"""
    if filter_type == 'low_pe':
        return stocks.filter(pe_ratio__lt=15)
    elif filter_type == 'high_dividend':
        return stocks.filter(dividend_yield__gt=0.03)
    elif filter_type == 'strong_growth':
        return stocks.filter(eps_growth__gt=0.15)
    elif filter_type == 'below_book':
        return stocks.filter(price_to_book__lt=1)
    elif filter_type == 'oversold':
        return stocks.filter(rsi__lt=30)
    return stocks

def home(request):
    return render(request,"stocks/home.html")