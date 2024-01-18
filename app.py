import requests
import os
import logging
from flask import Flask, render_template, request

app = Flask(__name__)

def get_class_for_rate(rate):
    """Determine the CSS class based on rate value."""
    if rate is None:
        return 'medium'
    if rate >= 94:
        return 'vhigh'
    elif rate >= 92:
        return 'high'
    elif rate <= 88:
        return 'vlow'
    elif rate <= 90:
        return 'low'
    else:
        return 'medium'

def get_class_for_change(change):
    """Determine the CSS class based on change percentage."""
    change =  float(change)
    if change is None:
        return 'medium'
    if change >= 10:
        return 'vhigh'
    elif change >= 5:
        return 'high'
    elif change <= -10:
        return 'vlow'
    elif change <= -5:
        return 'low'
    else:
        return 'medium'

def get_crypto_prices(symbols):
    """Get the prices, 24h changes, 1h changes, 7d changes, and market caps of multiple cryptocurrencies."""
    api_key = os.getenv("COINMARKETCAP_API_KEY")
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'symbol': ','.join(symbols),
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }

    try:
        response = requests.get(url, headers=headers, params=parameters)
        if response.status_code == 200:
            data = response.json()
            prices = {}
            for symbol in symbols:
                if symbol in data['data']:
                    quote = data['data'][symbol]['quote']['USD']
                    price = "{:.2f}".format(quote['price']) if quote['price'] is not None else None
                    price_change_1h = "{:.2f}".format(quote['percent_change_1h']) if quote['percent_change_1h'] is not None else None
                    price_change_24h = "{:.2f}".format(quote['percent_change_24h']) if quote['percent_change_24h'] is not None else None
                    price_change_7d = "{:.2f}".format(quote['percent_change_7d']) if quote['percent_change_7d'] is not None else None
                    market_cap = int(quote['market_cap']/1000000) if quote['market_cap'] is not None else None
                    prices[symbol] = (price if price is not None else None, 
                                      price_change_1h if price_change_1h is not None else None,
                                      price_change_24h if price_change_24h is not None else None,
                                      price_change_7d if price_change_7d is not None else None,
                                      market_cap if market_cap is not None else None)
                else:
                    logging.warning(f"Symbol {symbol} not found in API response")
                    prices[symbol] = (None, None, None, None, None)
            return prices
        else:
            logging.error(f"API request failed with status code {response.status_code}")
            return {symbol: (None, None, None, None, None) for symbol in symbols}
    except requests.exceptions.RequestException as e:
        logging.error(f"API request exception: {e}")
        return {symbol: (None, None, None, None, None) for symbol in symbols}

@app.route('/')
@app.route('/sort/<column>/<order>')
def index(column='market_cap', order='desc'):

    cryptos = [
        ('assets/btc.png', 'BTC'    , '96.87' ),
        ('assets/eth.png', 'ETH'    , '96.23' ),
        ('assets/bnb.png', 'BNB'    , '92.57' ),
        ('assets/sol.png', 'SOL'    , '91.96' ),
        ('assets/xrp.png', 'XRP'    , '94.25' ),
        ('assets/ada.png', 'ADA'    , '89.19' ),
        ('assets/avax.png', 'AVAX'  , '94.12' ),
        ('assets/doge.png', 'DOGE'  , '86.88' ),
        ('assets/trx.png', 'TRX'    , '88.20' ),
        ('assets/dot.png', 'DOT'    , '83.80' ),
        ('assets/link.png', 'LINK'  , '87.03' ),
        ('assets/icp.png', 'ICP'    , '81.78' ),
        ('assets/wemix.png', 'WEMIX', '93.91' ),
        ('assets/matic.png', 'MATIC', '93.27' ),
        ('assets/ton.png', 'TON'    , '92.91' ),
        ('assets/shib.png', 'SHIB'  , '90.81' ),
        ('assets/uni.png', 'UNI'    , '94.28' ),
        ('assets/atom.png', 'ATOM'  , '94.25' ),
        ('assets/ltc.png', 'LTC'    , '77.24' ),
        ('assets/bch.png', 'BCH'    , '74.16' ),
        ('assets/leo.png', 'LEO'    , '86.06' ),
        ('assets/inj.png', 'INJ'    , '84.13' ),
        ('assets/xlm.png', 'XLM'    , '85.97' ),
        ('assets/near.png', 'NEAR'  , '90.96' ),
        ('assets/op.png', 'OP'      , '88.60' ),
        ('assets/okb.png', 'OKB'    , '92.69' ),
        ('assets/apt.png', 'APT'    , '94.28' ),
        ('assets/tia.png', 'TIA'    , '69.14' ),
        ('assets/xmr.png', 'XMR'    , '73.35' ),
        ('assets/ldo.png', 'LDO'    , '91.64' ),
        ('assets/fil.png', 'FIL'    , '79.86' ),
        ('assets/arb.png', 'ARB'    , '94.30' ),
        ('assets/hbar.png', 'HBAR'  , '83.21' ),
        ('assets/imx.png', 'IMX'    , '89.76' ),
        ('assets/sei.png', 'SEI'    , '90.37' ),
        ('assets/rune.png', 'RUNE'  , '89.75' ),
        ('assets/sand.png', 'SAND'  , '93.39' ),
        ('assets/theta.png', 'THETA', '91.59' ),
        ('assets/chz.png', 'CHZ'    , '92.30' ),
        ('assets/gala.png', 'GALA'  , '94.59' ),
        ('assets/cake.png', 'CAKE'  , '93.49' ),
        ('assets/frax.png', 'FRAX'  , '91.59' ),
        ('assets/1inch.png', '1INCH', '93.07' ),
        ('assets/fet.png', 'FET'    , '91.97' ),
        ('assets/axl.png', 'AXL'    , '92.41' ),
        ('assets/twt.png', 'TWT'    , '92.84' ),
        ('assets/core.png', 'CORE'  , '90.39' ),
        ('assets/enj.png', 'ENJ'    , '92.08' ),
        ('assets/ftn.png', 'FTN'    , '90.45' ),
        ('assets/paxg.png', 'PAXG'  , '93.61' ),
        ('assets/iotx.png', 'IOTX'  , '92.30' ),
        ('assets/trb.png', 'TRB'    , '91.30' ),
        ('assets/floki.png', 'FLOKI', '91.93' ),
        ('assets/sxp.png', 'SXP'    , '91.62' ),
        ('assets/sfund.png', 'SFUND', '90.11' ),
    ]
    
    symbols = [crypto[1] for crypto in cryptos]
    prices = get_crypto_prices(symbols)

    updated_cryptos = []
    for crypto in cryptos:
        symbol = crypto[1]
        price, change_1h, change_24h, change_7d, market_cap = prices.get(symbol, (None, None, None, None, None))
        rate_class = get_class_for_rate(float(crypto[2]))
        change_1h_class = get_class_for_change(change_1h)
        change_24h_class = get_class_for_change(change_24h)
        change_7d_class = get_class_for_change(change_7d)
        updated_cryptos.append(crypto + (price, change_1h, change_24h, change_7d, market_cap, rate_class, change_24h_class, change_1h_class, change_7d_class))


    if column and order:
        reverse_order = True if order == 'desc' else False

        def get_sort_key(crypto, col):
            """Helper function to get the correct sort key based on column."""
            column_keys = {
                'rate': 2, 'price': 3, 'change_1h': 4, 'change_24h': 5,
                'change_7d': 6, 'market_cap': 7
            }


            # For other columns, sort based on their respective keys
            key = crypto[column_keys[col]]
            if key is None:
                return 0
            try:
                return float(key)
            except ValueError:
                return key

        cryptos = sorted(updated_cryptos, key=lambda x: get_sort_key(x, column), reverse=reverse_order)

        # Toggle the sorting order for the next click
        next_order = 'asc' if reverse_order else 'desc'


    return render_template('index.html', cryptos=cryptos, next_order=next_order)

if __name__ == '__main__':
    app.run(debug=True)