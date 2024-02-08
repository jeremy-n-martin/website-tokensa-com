from flask import Flask, render_template, request
from flask_caching import Cache
import requests
import os
import logging

app = Flask(__name__)

# Configure cache
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})

def get_class_for_rate_ck(rate):
    """Determine the CSS class based on rate value."""
    if rate == None: return 'medium'
    if rate == 00 :return 'low'
    if rate >= 93: return 'vhigh'
    elif rate >= 91: return 'high'
    elif rate <= 76: return 'vlow'
    elif rate <= 80: return 'low'
    else: return 'medium'

def get_class_for_rate_cb(rate):
    """Determine the CSS class based on rate value."""
    if rate == None: return 'medium'
    if rate == 00 :return 'low'
    if rate >= 97: return 'vhigh'
    elif rate >= 93: return 'high'
    elif rate <= 85: return 'vlow'
    elif rate <= 89: return 'low'
    else: return 'medium'

def get_class_for_rate_ti(rate):
    """Determine the CSS class based on rate value."""
    if rate == None:return 'medium'
    if rate == 00 :return 'low'
    if rate >= 69: return 'vhigh'
    elif rate >= 64: return 'high'
    elif rate <= 54: return 'vlow'
    elif rate <= 59: return 'low'
    else: return 'medium'

def get_class_for_rate_co(rate):
    """Determine the CSS class based on rate value."""
    if rate == None: return 'medium'
    if rate == 00 :return 'low'
    if rate >= 90: return 'vhigh'
    elif rate >= 82: return 'high'
    elif rate <= 50: return 'vlow'
    elif rate <= 58: return 'low'
    else: return 'medium'
    
def get_class_for_change(change, scale=1):
    if change is None:return 'medium'
    """Determine the CSS class based on change percentage."""
    change =  float(change)
    if change >= 2*scale:
        return 'vhigh'
    elif change >= scale:
        return 'high'
    elif change <= -2*scale:
        return 'vlow'
    elif change <= -scale:
        return 'low'
    else:
        return None

@cache.memoize(timeout=60)
def get_crypto_prices(symbols):
    
    """Get the prices, 24h changes, 1h changes, 7d changes, and market caps of multiple cryptocurrencies."""
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'symbol': ','.join(symbols),
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': os.getenv("COINMARKETCAP_API_KEY"),
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
                    prices[symbol] = (market_cap if market_cap is not None else None,
                                      price if price is not None else None, 
                                      price_change_1h if price_change_1h is not None else None,
                                      price_change_24h if price_change_24h is not None else None,
                                      price_change_7d if price_change_7d is not None else None)
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
        
@cache.memoize(timeout=1000)
def get_ti_prices():
    url = "https://api.tokeninsight.com/api/v1/rating/coins"

    headers = {
        "accept": "application/json",
        "TI_API_KEY": os.getenv("TOKENINSIGHT_API_KEY"),
    }

    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON data directly from the response
        data = response.json()

        # Extract the list of items (cryptocurrencies)
        items = data["data"]["items"]

        # Extract the symbol and rating_score for each item
        crypto_info = [(item["symbol"], item["rating_score"]) for item in items]

        return crypto_info
    else:
        print(f"Failed to fetch data from token insigh API: {response.status_code}")
        exit


@app.route('/')
@app.route('/sort/<column>/<order>')
def index(column='market_cap', order='desc'):

    #rajouter une colonne avec les layer etc
    #rajouter une colonne liquidity Volume/Market cap (24h)
    #rajouter une colonne avec les cotes binance etc
    cryptos = [
        ('assets/btc.png', 'BTC', '2009', '96', '95', '78'),
        ('assets/eth.png', 'ETH', '2015', '96', '96', '82'),
        ('assets/bnb.png', 'BNB', '2017', '92', '93', '77'),
        ('assets/sol.png', 'SOL', '2020', '91', '97', '62'),
        ('assets/xrp.png', 'XRP', '2012', '94', '95', '68'),
        ('assets/ada.png', 'ADA', '2017', '89', '95', '65'),
        ('assets/avax.png', 'AVAX', '2020', '94', '97', '71'),
        ('assets/doge.png', 'DOGE', '2013', '86', '97', '00'),
        ('assets/trx.png', 'TRX', '2018', '88', '90', '62'),
        ('assets/link.png', 'LINK', '2017', '87', '94', '75'),
        ('assets/dot.png', 'DOT', '2020', '83', '96', '70'),
        ('assets/ton.png', 'TON', '2022', '93', '96', '63'),
        ('assets/matic.png', 'MATIC', '2017', '93', '96', '70'),
        ('assets/shib.png', 'SHIB', '2020', '91', '92', '00'),
        ('assets/ltc.png', 'LTC', '2011', '77', '88', '56'),
        ('assets/icp.png', 'ICP', '2021', '81', '97', '00'),
        ('assets/bch.png', 'BCH', '2017', '74', '88', '53'),
        ('assets/uni.png', 'UNI', '2018', '94', '95', '75'),
        ('assets/atom.png', 'ATOM', '2019', '94', '88', '71'),
        ('assets/leo.png', 'LEO', '2019', '86', '88', '54'),
        ('assets/etc.png', 'ETC', '2016', '77', '88', '57'),
        ('assets/xlm.png', 'XLM', '2014', '85', '89', '63'),
        ('assets/okb.png', 'OKB', '2019', '92', '97', '67'),
        ('assets/inj.png', 'INJ', '2020', '84', '97', '68'),
        ('assets/op.png', 'OP', '2021', '88', '94', '62'),
        ('assets/near.png', 'NEAR', '2020', '90', '88', '70'),
        ('assets/apt.png', 'APT', '2022', '94', '97', '63'),
        ('assets/tia.png', 'TIA', '2023', '69', '97', '57'),
        ('assets/xmr.png', 'XMR', '2014', '73', '88', '63'),
        ('assets/ldo.png', 'LDO', '2020', '91', '96', '71'),
        ('assets/fil.png', 'FIL', '2020', '79', '89', '67'),
        ('assets/hbar.png', 'HBAR', '2019', '83', '90', '66'),
        ('assets/imx.png', 'IMX', '2021', '89', '95', '64'),
        ('assets/arb.png', 'ARB', '2023', '94', '89', '57'),
        ('assets/kas.png', 'KAS', '2021', '00', '00', '00'),
        ('assets/mnt.png', 'MNT', '2023', '81', '93', '00'),
        ('assets/stx.png', 'STX', '2019', '78', '88', '76'),
        ('assets/cro.png', 'CRO', '2018', '92', '88', '63'),
        ('assets/vet.png', 'VET', '2018', '92', '97', '64'),
        ('assets/mkr.png', 'MKR', '2015', '91', '90', '68'),
        ('assets/sei.png', 'SEI', '2023', '90', '96', '57'),
        ('assets/rndr.png', 'RNDR', '2020', '59', '97', '60'),
        ('assets/ordi.png', 'ORDI', '2023', '52', '00', '00'),
        ('assets/bsv.png', 'BSV', '2018', '70', '00', '00'),
        ('assets/grt.png', 'GRT', '2020', '00', '97', '68'),
        ('assets/algo.png', 'ALGO', '2019', '87', '97', '67'),
        ('assets/aave.png', 'AAVE', '2020', '85', '91', '69'),
        ('assets/rune.png', 'RUNE', '2018', '89', '00', '00'),
        ('assets/qnt.png', 'QNT', '2018', '77', '84', '54'),
        ('assets/egld.png', 'EGLD', '2020', '90', '95', '00'),
        ('assets/sui.png', 'SUI', '2023', '83', '95', '60'),
        ('assets/mina.png', 'MINA', '2021', '73', '97', '64'),
        ('assets/sats.png', '1000SATS', '2022', '56', '00', '00'),
        ('assets/flow.png', 'FLOW', '2020', '79', '91', '67'),
        ('assets/hnt.png', 'HNT', '2019', '73', '97', '66'),
        ('assets/ftm.png', 'FTM', '2019', '89', '97', '66'),
        ('assets/snx.png', 'SNX', '2018', '84', '96', '00'),
        ('assets/sand.png', 'SAND', '2020', '93', '97', '68'),
        ('assets/axs.png', 'AXS', '2020', '85', '92', '66'),
        ('assets/xtz.png', 'XTZ', '2018', '86', '84', '00'),
        ('assets/theta.png', 'THETA', '2019', '91', '84', '00'),
        ('assets/kcs.png', 'KCS', '2017', '76', '89', '00'),
        ('assets/btt.png', 'BTT', '2019', '78', '93', '00'),
        ('assets/beam.png', 'BEAM', '2019', '67', '84', '00'),
        ('assets/astr.png', 'ASTR', '2022', '83', '97', '00'),
        ('assets/wemix.png', 'WEMIX', '2022', '93', '00', '00'),
        ('assets/dydx.png', 'ETHDYDX', '2021', '44', '85', '00'),
        ('assets/ftt.png', 'FTT', '2019', '67', '00', '00'),
        ('assets/mana.png', 'MANA', '2017', '85', '88', '66'),
        ('assets/bgb.png', 'BGB', '2021', '75', '91', '00'),
        ('assets/blur.png', 'BLUR', '2022', '71', '94', '00'),
        ('assets/neo.png', 'NEO', '2016', '73', '94', '59'),
        ('assets/osmo.png', 'OSMO', '2021', '00', '00', '00'),
        ('assets/chz.png', 'CHZ', '2019', '92', '97', '00'),
        ('assets/eos.png', 'EOS', '2018', '82', '89', '59'),
        ('assets/flr.png', 'FLR', '2022', '73', '88', '55'),
        ('assets/kava.png', 'KAVA', '2019', '86', '00', '00'),
        ('assets/bonk.png', 'BONK', '2022', '60', '85', '00'),
        ('assets/woo.png', 'WOO', '2021', '86', '95', '00'),
        ('assets/iota.png', 'IOTA', '2016', '73', '90', '60'),
        ('assets/klay.png', 'KLAY', '2019', '85', '96', '00'),
        ('assets/cfx.png', 'CFX', '2020', '71', '89', '59'),
        ('assets/xdc.png', 'XDC', '2019', '52', '00', '51'),
        ('assets/rose.png', 'ROSE', '2020', '79', '91', '00'),
        ('assets/cake.png', 'CAKE', '2020', '94', '93', '00'),
        ('assets/fxs.png', 'FXS', '2020', '81', '94', '00'),
        ('assets/gala.png', 'GALA', '2020', '94', '84', '58'),
        ('assets/xec.png', 'XEC', '2021', '71', '90', '00'),
        ('assets/ar.png', 'AR', '2018', '69', '91', '00'),
        ('assets/lunc.png', 'LUNC', '2022', '49', '00', '00'),
        ('assets/sc.png', 'SC', '2015', '67', '92', '00'),
        ('assets/rpl.png', 'RPL', '2017', '77', '93', '54'),
        ('assets/akt.png', 'AKT', '2020', '74', '94', '00'),
        ('assets/ens.png', 'ENS', '2021', '85', '93', '00'),
        ('assets/ron.png', 'RON', '2021', '86', '92', '00'),
        ('assets/manta.png', 'MANTA', '2024', '71', '92', '00'),
        ('assets/crv.png', 'CRV', '2020', '66', '92', '66'),
        ('assets/gno.png', 'GNO', '2017', '77', '87', '00'),
        ('assets/fet.png', 'FET', '2019', '91', '77', '54'),
        ('assets/pendle.png', 'PENDLE', '2023', '81', '83', '65'),
        ('assets/cspr.png', 'CSPR', '2021', '80', '92', '59'),
        ('assets/ape.png', 'APE', '2022', '93', '92', '60'),
        ('assets/axl.png', 'AXL', '2022', '92', '84', '54'),
        ('assets/nexo.png', 'NEXO', '2018', '77', '92', '00'),
        ('assets/gt.png', 'GT', '2019', '87', '76', '00'),
        ('assets/pyth.png', 'PYTH', '2023', '89', '92', '00'),
        ('assets/gmt.png', 'GMT', '2022', '76', '92', '00'),
        ('assets/pepe.png', 'PEPE', '2023', '87', '90', '00'),
        ('assets/1inch.png', '1INCH', '2020', '93', '92', '00'),
        ('assets/xrd.png', 'XRD', '2021', '73', '92', '00'),
        ('assets/uma.png', 'UMA', '2020', '73', '92', '00'),
        ('assets/twt.png', 'TWT', '2020', '93', '92', '68'),
        ('assets/comp.png', 'COMP', '2020', '86', '50', '50'),
        ('assets/core.png', 'CORE', '2023', '90', '83', '00'),
        ('assets/gmx.png', 'GMX', '2021', '91', '90', '64'),
        ('assets/gas.png', 'GAS', '2017', '60', '92', '00'),
        ('assets/nft.png', 'NFT', '2021', '61', '78', '49'),
        ('assets/xem.png', 'XEM', '2015', '61', '00', '00'),
        ('assets/luna.png', 'LUNA', '2019', '59', '92', '00'),
        ('assets/metis.png', 'METIS', '2021', '58', '90', '00'),
        ('assets/elf.png', 'ELF', '2017', '70', '92', '00'),
        ('assets/btg.png', 'BTG', '2017', '46', '00', '00'),
        ('assets/skl.png', 'SKL', '2020', '85', '92', '00'),
        ('assets/enj.png', 'ENJ', '2017', '92', '92', '65'),
        ('assets/iotx.png', 'IOTX', '2018', '92', '92', '67'),
        ('assets/zec.png', 'ZEC', '2016', '73', '82', '00'),
        ('assets/zil.png', 'ZIL', '2018', '80', '92', '00'),
        ('assets/wif.png', 'WIF', '2023', '00', '00', '00'),
        ('assets/celo.png', 'CELO', '2020', '73', '92', '00'),
        ('assets/deso.png', 'DESO', '2021', '72', '84', '00'),
        ('assets/ht.png', 'HT', '2018', '79', '87', '55'),
        ('assets/ntrn.png', 'NTRN', '2015', '67', '88', '00'),
        ('assets/bat.png', 'BAT', '2017', '91', '85', '00'),
        ('assets/mask.png', 'MASK', '2021', '00', '92', '57'),
        ('assets/agix.png', 'AGIX', '2017', '81', '92', '63'),
        ('assets/ksm.png', 'KSM', '2017', '72', '85', '00'),
        ('assets/trb.png', 'TRB', '2019', '91', '78', '55'),
        ('assets/hot.png', 'HOT', '2018', '00', '00', '00'),
        ('assets/lrc.png', 'LRC', '2017', '85', '00', '00'),
        ('assets/dash.png', 'DASH', '2014', '73', '89', '00'),
        ('assets/qtum.png', 'QTUM', '2017', '73', '92', '00'),
        ('assets/xch.png', 'XCH', '2021', '72', '92', '00'),
        ('assets/ilv.png', 'ILV', '2021', '78', '92', '00'),
        ('assets/ethw.png', 'ETHW', '2022', '70', '76', '00'),
        ('assets/glmr.png', 'GLMR', '2022', '80', '92', '00'),
        ('assets/ssv.png', 'SSV', '2021', '69', '92', '54'),
        ('assets/super.png', 'SUPER', '2021', '82', '92', '00'),
        ('assets/sfp.png', 'SFP', '2021', '91', '85', '50'),
        ('assets/tfuel.png', 'TFUEL', '2019', '72', '91', '00'),
        ('assets/ray.png', 'RAY', '2021', '72', '00', '00'),
        ('assets/t.png', 'T', '2022', '85', '85', '00'),
        ('assets/wld.png', 'WLD', '2023', '82', '89', '00'),
        ('assets/kda.png', 'KDA', '2019', '00', '00', '00'),
        ('assets/jto.png', 'JTO', '2023', '69', '69', '00'),
        ('assets/magic.png', 'MAGIC', '2021', '78', '86', '53'),
        ('assets/floki.png', 'FLOKI', '2021', '91', '92', '00'),
        ('assets/ant.png', 'ANT', '2017', '76', '89', '55'),
        ('assets/mx.png', 'MX', '2018', '77', '85', '55'),
        ('assets/cvx.png', 'CVX', '2021', '86', '85', '53'),
        ('assets/cfg.png', 'CFG', '2021', '81', '00', '00'),
        ('assets/zrx.png', 'ZRX', '2017', '83', '00', '70'),
        ('assets/waves.png', 'WAVES', '2016', '73', '83', '00'),
        ('assets/jst.png', 'JST', '2020', '75', '00', '00'),
        ('assets/rbn.png', 'RBN', '2021', '70', '89', '00'),
        ('assets/rvn.png', 'RVN', '2018', '72', '90', '00'),
        ('assets/yfi.png', 'YFI', '2020', '69', '92', '63'),
        ('assets/trac.png', 'TRAC', '2018', '70', '91', '53'),
        ('assets/sushi.png', 'SUSHI', '2020', '82', '92', '60'),
        ('assets/jasmy.png', 'JASMY', '2021', '83', '82', '00'),
        ('assets/dcr.png', 'DCR', '2016', '67', '87', '00'),
        ('assets/ankr.png', 'ANKR', '2018', '87', '88', '62'),
        ('assets/xai.png', 'XAI', '2024', '00', '50', '50'),
        ('assets/ocean.png', 'OCEAN', '2019', '89', '91', '62'),
        ('assets/bico.png', 'BICO', '2021', '78', '90', '54'),
        ('assets/mobile.png', 'MOBILE', '2022', '66', '50', '50'),
        ('assets/icx.png', 'ICX', '2017', '81', '89', '00'),
        ('assets/storj.png', 'STORJ', '2017', '87', '81', '00'),
        ('assets/audio.png', 'AUDIO', '2020', '72', '92', '00'),
        ('assets/glm.png', 'GLM', '2016', '76', '92', '00'),
        ('assets/lpt.png', 'LPT', '2018', '78', '88', '00'),
        ('assets/bal.png', 'BAL', '2020', '68', '00', '00'),
        ('assets/band.png', 'BAND', '2019', '88', '90', '60'),
        ('assets/meme.png', 'MEME', '2023', '89', '87', '00'),
        ('assets/movr.png', 'MOVR', '2021', '70', '80', '00'),
        ('assets/ont.png', 'ONT', '2018', '79', '92', '00'),
        ('assets/fnsa.png', 'FNSA', '2020', '89', '83', '00'),
        ('assets/sxp.png', 'SXP', '2019', '91', '00', '00'),
        ('assets/waxp.png', 'WAXP', '2017', '81', '91', '00'),
        ('assets/hex.png', 'HEX', '2019', '00', '00', '00'),
        ('assets/tao.png', 'TAO', '2023', '59', '90', '00'),
        ('assets/cheel.png', 'CHEEL', '2023', '89', '92', '53'),
        ('assets/frax.png', 'FRAX', '2020', '91', '92', '60'),
        ('assets/pokt.png', 'POKT', '2020', '00', '89', '00'),
        ('assets/kuji.png', 'KUJI', '2021', '79', '74', '00'),
        ('assets/rlb.png', 'RLB', '2021', '00', '00', '00'),
        ('assets/lyx.png', 'LYX', '2020', '00', '00', '00'),
        ('assets/flex.png', 'FLEX', '2019', '88', '75', '00'),
        ('assets/azero.png', 'AZERO', '2021', '73', '92', '00'),
        ('assets/strd.png', 'STRD', '2022', '00', '77', '56'),
        ('assets/orbr.png', 'ORBR', '2022', '48', '77', '37'),
        ('assets/one.png', 'ONE', '2019', '77', '92', '00'),
        ('assets/ftn.png', 'FTN', '2023', '90', '83', '52'),
        ('assets/prime.png', 'PRIME', '2022', '70', '92', '00'),
        ('assets/ctsi.png', 'CTSI', '2020', '92', '92', '53'),
        ('assets/sfund.png', 'SFUND', '2021', '90', '00', '00'),
    ]

    # the token insight prices maj
    prices = get_ti_prices()
    for symbol, score in prices:
        updated_cryptos = []
        for item in cryptos:
            if item[1] == symbol:
                score = round(float(score))
                new_item = item[:5] + (score,)
            else:
                new_item = item
            updated_cryptos.append(new_item)
        cryptos = updated_cryptos
    
    symbols = [crypto[1] for crypto in cryptos]
    prices = get_crypto_prices(symbols)
    updated_cryptos = []

    for crypto in cryptos:
        symbol = crypto[1]
        market_cap, price, change_1h, change_24h, change_7d = prices.get(symbol, (None, None, None, None, None))
        rate_ck_class = get_class_for_rate_ck(float(crypto[3]))
        rate_cb_class = get_class_for_rate_cb(float(crypto[4]))
        rate_ti_class = get_class_for_rate_ti(float(crypto[5]))
        rate_consolided = (float(crypto[3]) + 0.9*float(crypto[4]) + 1.1*float(crypto[5]))/3
        rate_co_class = get_class_for_rate_co(float(rate_consolided))
        rate_co = str(round(rate_consolided))

        change_1h_class = get_class_for_change(change_1h, scale=1)
        change_24h_class = get_class_for_change(change_24h, scale=5)
        change_7d_class = get_class_for_change(change_7d, scale=10)
        updated_cryptos.append(crypto + (price, change_1h, change_24h, change_7d, market_cap, rate_co,
                                         rate_ck_class, rate_cb_class, rate_ti_class, change_24h_class,
                                         change_1h_class, change_7d_class, rate_co_class))


    if column and order:
        reverse_order = True if order == 'desc' else False

        def get_sort_key(crypto, col):
            """Helper function to get the correct sort key based on column."""
            column_keys = {
                'creation_time': 2,
                'rate_ck': 3, 'rate_cb': 4, 'rate_ti': 5, 'price': 6, 'change_1h': 7,
                'change_24h': 8, 'change_7d': 9, 'market_cap': 10, 'rate_co' : 11,
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