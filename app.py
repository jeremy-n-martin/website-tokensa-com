import requests
from bs4 import BeautifulSoup
from flask import Flask

app = Flask(__name__)



@app.route('/')
def hello():
    cryptos = get_cryptocurrencies('https://coinmarketcap.com/')
    for name, market_cap in cryptos:
        print(f"{name}: {market_cap}")
    return

if __name__ == '__main__':
    app.run(debug=True)
    



def get_cryptocurrencies(url):
    # Fetch the content from the URL
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # Find the table or section that lists the cryptocurrencies
    # (This step may require adjustment depending on the page structure)
    crypto_table = soup.find('table', {'class': 'cmc-table'})  # Example class name

    # Iterate through the table rows and extract name and market cap
    cryptos = []
    for row in crypto_table.find_all('tr')[1:]:  # Skipping the header row
        columns = row.find_all('td')
        name = columns[2].text.strip()  # Example column index for name
        market_cap = columns[3].text.strip()  # Example column index for market cap
        cryptos.append((name, market_cap))

    return cryptos