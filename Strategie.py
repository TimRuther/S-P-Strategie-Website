from flask import Flask, render_template, jsonify
import requests

app = Flask(__name__)

API_KEY = "QC02NWH08MJ6MYDC"  # dein Alpha Vantage API-Schlüssel
SYMBOL = 'SPX'  # Symbol für den S&P 500

# Funktion, um S&P 500-Daten abzurufen
def get_sp500_data():
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={SYMBOL}&apikey={API_KEY}'
    response = requests.get(url)
    data = response.json().get('Time Series (Daily)', {})
    return data

# Funktion zur Berechnung des 200-Tage-SMA
def calculate_sma(data, period=200):
    closing_prices = [float(value['4. close']) for key, value in sorted(data.items(), reverse=True)]
    sma = sum(closing_prices[:period]) / period if len(closing_prices) >= period else None
    return sma

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sma-status', methods=['GET'])
def sma_status():
    data = get_sp500_data()
    sma_200 = calculate_sma(data)
    current_price = float(next(iter(data.values()))['4. close'])  # Neuester Schlusskurs
    
    if current_price > sma_200:
        status = "Der Preis liegt über dem 200-Tage-SMA."
    else:
        status = "Der Preis liegt unter dem 200-Tage-SMA."
    
    return jsonify({
        'current_price': current_price,
        'sma_200': sma_200,
        'status': status
    })

if __name__ == '__main__':
    app.run(debug=True)
