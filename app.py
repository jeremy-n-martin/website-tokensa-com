import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    cryptos = [
        ('assets/btc.png', 'BTC', '96.87', '83400'),
        ('assets/eth.png', 'ETH', '96.23', '30500'),
        ('assets/bnb.png', 'BNB', '92.57', '4629'),
        ('assets/sol.png', 'SOL', '91.96', '4240'),
        ('assets/xrp.png', 'XRP', '94.25', '3124'),
        ('assets/ada.png', 'ADA', '89.19', '1930'),
        ('assets/avax.png', 'AVAX', '94.12', '1348'),
        ('assets/doge.png', 'DOGE', '86.88', '1175'),
        ('assets/tron.png', 'TRON', '88.20', '1005'),
        ('assets/dot.png', 'DOT', '83.80', '979'),
        ('assets/link.png', 'LINK', '87.03', '860'),
        ('assets/wemix.png', 'WEMIX', '93.91', '1462'),
        ('assets/matic.png', 'MATIC', '93.27', '844'),
        ('assets/ton.png', 'TON', '92.91', '731'),
        ('assets/shib.png', 'SHIB', '90.81', '585'),
        ('assets/atom.png', 'ATOM', '94.25', '392'),
        ('assets/apt.png', 'APT', '94.28', '334'),
        ('assets/imx.png', 'IMX', '89.76', '277'),
        ('assets/sei.png', 'SEI', '90.37', '170'),
        ('assets/rune.png', 'RUNE', '89.75', '156'),
        ('assets/sand.png', 'SAND', '93.39', '108'),
        ('assets/theta.png', 'THETA', '91.59', '106'),
        ('assets/chz.png', 'CHZ', '92.30', '77'),
        ('assets/gala.png', 'GALA', '94.59', '74'),
        ('assets/cake.png', 'CAKE', '93.49', '72'),
        ('assets/frax.png', 'FRAX', '91.59', '64'),
        ('assets/1inch.png', '1INCH', '93.07', '56'),
        ('assets/fet.png', 'FET', '91.97', '56'),
        ('assets/axl.png', 'AXL', '92.41', '56'),
        ('assets/twt.png', 'TWT', '92.84', '48'),
        ('assets/core.png', 'CORE', '90.39', '44'),
        ('assets/enj.png', 'ENJ', '92.08', '43'),
        ('assets/ftn.png', 'FTN', '90.45', '43'),
        ('assets/paxg.png', 'PAXG', '93.61', '42'),
        ('assets/iotx.png', 'IOTX', '92.30', '40'),
        ('assets/trb.png', 'TRB', '91.30', '31'),
        ('assets/floki.png', 'FLOKI', '91.93', '29'),
        ('assets/sxp.png', 'SXP', '91.62', '21'),
        ('assets/sfund.png', 'SFUND', '90.11', '19'),
    ]
    sorted_cryptos = sorted(cryptos, key=lambda x: int(x[3]), reverse=True)
    return render_template('index.html', cryptos=sorted_cryptos)



if __name__ == '__main__':
    app.run(debug=True)
