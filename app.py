import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template

app = Flask(__name__)

def get_cryptocurrencies(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    crypto_table = soup.find('table', {'class': 'cmc-table'})  # Adjust class as needed
    cryptos = []

    for row in crypto_table.find_all('tr')[1:]:  # Skip header
        columns = row.find_all('td')
        name = columns[2].text.strip()  # Adjust index as needed
        market_cap = columns[3].text.strip()  # Adjust index as needed
        cryptos.append((name, market_cap))

    return cryptos

@app.route('/')
def show_cryptocurrencies():
    url = 'https://coinmarketcap.com/'
    cryptos = get_cryptocurrencies(url)
    return render_template('cryptos.html', cryptos=cryptos)

if __name__ == '__main__':
    app.run(debug=True)
