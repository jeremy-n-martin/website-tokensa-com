import requests
import os
from bs4 import BeautifulSoup
from flask import Flask, render_template


app = Flask(__name__)

def get_crypto_price(symbol):
    """Récupère le prix d'une crypto-monnaie et le changement sur 24h depuis l'API Binance."""
    url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}USDT"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        last_price = float(data['lastPrice']) if 'lastPrice' in data else None
        price_change_percent = float(data['priceChangePercent']) if 'priceChangePercent' in data else None
        return last_price, round(price_change_percent, 2)
    else:
        return None, None
    
@app.route('/')
def index():

    cryptos = [
        ('assets/btc.png', 'BTC', '96.87', '8340'),
        ('assets/eth.png', 'ETH', '96.23', '3050'),
        ('assets/bnb.png', 'BNB', '92.57', '462'),
        ('assets/sol.png', 'SOL', '91.96', '424'),
        ('assets/xrp.png', 'XRP', '94.25', '312'),
        ('assets/ada.png', 'ADA', '89.19', '193'),
        ('assets/avax.png', 'AVAX', '94.12', '134'),
        ('assets/doge.png', 'DOGE', '86.88', '117'),
        ('assets/tron.png', 'TRON', '88.20', '100'),
        ('assets/dot.png', 'DOT', '83.80', '97'),
        ('assets/link.png', 'LINK', '87.03', '86'),
        ('assets/wemix.png', 'WEMIX', '93.91', '146'),
        ('assets/matic.png', 'MATIC', '93.27', '84'),
        ('assets/ton.png', 'TON', '92.91', '73'),
        ('assets/shib.png', 'SHIB', '90.81', '58'),
        ('assets/uni.png', 'UNI', '94.28', '41'),
        ('assets/atom.png', 'ATOM', '94.25', '39'),
        ('assets/leo.png', 'LEO', '86.06', '37'),
        ('assets/inj.png', 'INJ', '84.13', '34'),
        ('assets/apt.png', 'APT', '94.28', '33'),
        ('assets/imx.png', 'IMX', '89.76', '27'),
        ('assets/sei.png', 'SEI', '90.37', '17'),
        ('assets/rune.png', 'RUNE', '89.75', '15'),
        ('assets/sand.png', 'SAND', '93.39', '10'),
        ('assets/theta.png', 'THETA', '91.59', '10'),
        ('assets/chz.png', 'CHZ', '92.30', '7'),
        ('assets/gala.png', 'GALA', '94.59', '7'),
        ('assets/cake.png', 'CAKE', '93.49', '7'),
        ('assets/frax.png', 'FRAX', '91.59', '6'),
        ('assets/1inch.png', '1INCH', '93.07', '5'),
        ('assets/fet.png', 'FET', '91.97', '5'),
        ('assets/axl.png', 'AXL', '92.41', '5'),
        ('assets/twt.png', 'TWT', '92.84', '4'),
        ('assets/core.png', 'CORE', '90.39', '4'),
        ('assets/enj.png', 'ENJ', '92.08', '4'),
        ('assets/ftn.png', 'FTN', '90.45', '4'),
        ('assets/paxg.png', 'PAXG', '93.61', '4'),
        ('assets/iotx.png', 'IOTX', '92.30', '4'),
        ('assets/trb.png', 'TRB', '91.30', '3'),
        ('assets/floki.png', 'FLOKI', '91.93', '2'),
        ('assets/sxp.png', 'SXP', '91.62', '2'),
        ('assets/sfund.png', 'SFUND', '90.11', '1'),
    ]
    updated_cryptos = []
    for crypto in cryptos:
        symbol = crypto[1]
        #price, change_24h = get_crypto_price(symbol)
        #updated_cryptos.append(crypto + (price, change_24h))
    #cryptos = sorted(updated_cryptos, key=lambda x: int(x[5]) if x[5] is not None else 0, reverse=True)
    return render_template('index2.html', cryptos=cryptos)


if __name__ == '__main__':
    app.run(debug=True)
