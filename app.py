import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def show_cryptocurrencies():
    cryptos = [
        ('assets/gala.png', 'GALA', '94.59', '74'),
        ('assets/apt.png', 'APT', '94.28', '334'),
        ('assets/atom.png', 'ATOM', '94.25', '392'),
        ('assets/xrp.png', 'XRP', '94.25', '3124'),
        ('assets/wemix.png', 'WEMIX', '93.91', '1462'),
        ('assets/paxg.png', 'PAXG', '93.61', '42'),
        ('assets/cake.png', 'CAKE', '93.49', '72'),
        ('assets/sand.png', 'SAND', '93.39', '108'),
        ('assets/matic.png', 'MATIC', '93.27', '844'),
        ('assets/1inch.png', '1INCH', '93.07', '56'),
        ('assets/ton.png', 'TON', '92.91', '731')
    ]
    return render_template('cryptos.html', cryptos=cryptos)

if __name__ == '__main__':
    app.run(debug=True)
