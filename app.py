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
    elif rate <= 80:
        return 'vlow'
    elif rate <= 76:
        return 'low'
    else:
        return 'medium'

def get_class_for_change(change, scale=1):
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

@app.route('/')
@app.route('/sort/<column>/<order>')
def index(column='market_cap', order='desc'):

    #rajouter une colonne avec les cotes binance etc
    #rajouter une colonne avec les layer etc
    #rajouter une colonne avec les dates de création etc
    cryptos = [
        ('assets/btc.png', 'BTC'      , '96.87', '0' ),
        ('assets/eth.png', 'ETH'      , '96.23', '0' ),
        ('assets/bnb.png', 'BNB'      , '92.57', '0' ),
        ('assets/sol.png', 'SOL'      , '91.96', '0' ),
        ('assets/xrp.png', 'XRP'      , '94.25', '0' ),
        ('assets/ada.png', 'ADA'      , '89.19', '0' ),
        ('assets/avax.png', 'AVAX'    , '94.12', '0' ),
        ('assets/doge.png', 'DOGE'    , '86.88', '0' ),
        ('assets/trx.png', 'TRX'      , '88.20', '0' ),
        ('assets/dot.png', 'DOT'      , '83.80', '0' ),
        ('assets/link.png', 'LINK'    , '87.03', '0' ),
        ('assets/icp.png', 'ICP'      , '81.78', '0' ),
        ('assets/wemix.png', 'WEMIX'  , '93.91', '0' ),
        ('assets/matic.png', 'MATIC'  , '93.27', '0' ),
        ('assets/ton.png', 'TON'      , '92.91', '0' ),
        ('assets/shib.png', 'SHIB'    , '90.81', '0' ),
        ('assets/uni.png', 'UNI'      , '94.28', '0' ),
        ('assets/atom.png', 'ATOM'    , '94.25', '0' ),
        ('assets/ltc.png', 'LTC'      , '77.24', '0' ),
        ('assets/bch.png', 'BCH'      , '74.16', '0' ),
        ('assets/leo.png', 'LEO'      , '86.06', '0' ),
        ('assets/inj.png', 'INJ'      , '84.13', '0' ),
        ('assets/xlm.png', 'XLM'      , '85.97', '0' ),
        ('assets/near.png', 'NEAR'    , '90.96', '0' ),
        ('assets/op.png', 'OP'        , '88.60', '0' ),
        ('assets/okb.png', 'OKB'      , '92.69', '0' ),
        ('assets/apt.png', 'APT'      , '94.28', '0' ),
        ('assets/tia.png', 'TIA'      , '69.14', '0' ),
        ('assets/xmr.png', 'XMR'      , '73.35', '0' ),
        ('assets/ldo.png', 'LDO'      , '91.64', '0' ),
        ('assets/fil.png', 'FIL'      , '79.86', '0' ),
        ('assets/arb.png', 'ARB'      , '94.30', '0' ),
        ('assets/vet.png', 'VET'      , '50.00', '0' ),
        ('assets/mkr.png', 'MKR'      , '50.00', '0' ),
        ('assets/rndr.png', 'RNDR'    , '50.00', '0' ),
        ('assets/bsv.png', 'BSV'      , '50.00', '0' ),
        ('assets/grt.png', 'GRT'      , '50.00', '0' ),
        ('assets/algo.png', 'ALGO'    , '50.00', '0' ),
        ('assets/ordi.png', 'ORDI'    , '50.00', '0' ),
        ('assets/aave.png', 'AAVE'    , '50.00', '0' ),
        ('assets/egld.png', 'EGLD'    , '50.00', '0' ),
        ('assets/qnt.png', 'QNT'      , '50.00', '0' ),
        ('assets/sui.png', 'SUI'      , '50.00', '0' ),
        ('assets/mina.png', 'MINA'    , '50.00', '0' ),
        ('assets/sats.png', 'SATS'    , '50.00', '0' ),
        ('assets/flow.png', 'FLOW'    , '50.00', '0' ),
        ('assets/hnt.png', 'HNT'      , '50.00', '0' ),
        ('assets/ftm.png', 'FTM'      , '50.00', '0' ),
        ('assets/snx.png', 'SNX'      , '50.00', '0' ),
        ('assets/axs.png', 'AXS'      , '50.00', '0' ),
        ('assets/xtz.png', 'XTZ'      , '50.00', '0' ),
        ('assets/beam.png', 'BEAM'    , '50.00', '0' ),
        ('assets/btt.png', 'BTT'      , '50.00', '0' ),
        ('assets/kcs.png', 'KCS'      , '50.00', '0' ),
        ('assets/dydx.png', 'DYDX'    , '50.00', '0' ),
        ('assets/ftt.png', 'FTT'      , '50.00', '0' ),
        ('assets/astr.png', 'ASTR'    , '50.00', '0' ),
        ('assets/bgb.png', 'BGB'      , '50.00', '0' ),
        ('assets/blur.png', 'BLUR'    , '50.00', '0' ),
        ('assets/mana.png', 'MANA'    , '50.00', '0' ),
        ('assets/neo.png', 'NEO'      , '50.00', '0' ),
        ('assets/osmo.png', 'OSMO'    , '50.00', '0' ),
        ('assets/eos.png', 'EOS'      , '50.00', '0' ),
        ('assets/bonk.png', 'BONK'    , '50.00', '0' ),
        ('assets/cfx.png', 'CFX'      , '50.00', '0' ),
        ('assets/kava.png', 'KAVA'    , '50.00', '0' ),
        ('assets/woo.png', 'WOO'      , '50.00', '0' ),
        ('assets/klay.png', 'KLAY'    , '50.00', '0' ),
        ('assets/flr.png', 'FLR'      , '50.00', '0' ),
        ('assets/iota.png', 'IOTA'    , '50.00', '0' ),
        ('assets/rose.png', 'ROSE'    , '50.00', '0' ),
        ('assets/lunc.png', 'LUNC'    , '50.00', '0' ),
        ('assets/fxs.png', 'FXS'      , '50.00', '0' ),
        ('assets/xdc.png', 'XDC'      , '50.00', '0' ),
        ('assets/ens.png', 'ENS'      , '50.00', '0' ),
        ('assets/rpl.png', 'RPL'      , '50.00', '0' ),
        ('assets/xec.png', 'XEC'      , '50.00', '0' ),
        ('assets/sc.png', 'SC'        , '50.00', '0' ),
        ('assets/ar.png', 'AR'        , '50.00', '0' ),
        ('assets/akt.png', 'AKT'      , '50.00', '0' ),
        ('assets/manta.png', 'MANTA'  , '50.00', '0' ),
        ('assets/crv.png', 'CRV'      , '50.00', '0' ),
        ('assets/ron.png', 'RON'      , '50.00', '0' ),
        ('assets/cspr.png', 'CSPR'    , '50.00', '0' ),
        ('assets/ape.png', 'APE'      , '50.00', '0' ),
        ('assets/pyth.png', 'PYTH'    , '50.00', '0' ),
        ('assets/gmt.png', 'GMT'      , '50.00', '0' ),
        ('assets/pepe.png', 'PEPE'    , '50.00', '0' ),
        ('assets/nexo.png', 'NEXO'    , '50.00', '0' ),
        ('assets/gmt.png', 'GMT'      , '50.00', '0' ),
        ('assets/gt.png', 'GT'        , '50.00', '0' ),
        ('assets/pendle.png', 'PENDLE', '50.00', '0' ),
        ('assets/gas.png', 'GAS'      , '50.00', '0' ),
        ('assets/metis.png', 'METIS'  , '50.00', '0' ),
        ('assets/luna.png', 'LUNA'    , '50.00', '0' ),
        ('assets/comp.png', 'COMP'    , '50.00', '0' ),
        ('assets/xrd.png', 'XRD'      , '50.00', '0' ),
        ('assets/wif.png', 'WIF'      , '50.00', '0' ),
        ('assets/nft.png', 'NFT'      , '50.00', '0' ),
        ('assets/btg.png', 'BTG'      , '50.00', '0' ),
        ('assets/skl.png', 'SKL'      , '50.00', '0' ),
        ('assets/elf.png', 'ELF'      , '50.00', '0' ),
        ('assets/deso.png', 'DESO'    , '50.00', '0' ),
        ('assets/zil.png', 'ZIL'      , '50.00', '0' ),
        ('assets/celo.png', 'CELO'    , '50.00', '0' ),
        ('assets/zec.png', 'ZEC'      , '50.00', '0' ),
        ('assets/ntrn.png', 'NTRN'    , '50.00', '0' ),
        ('assets/xem.png', 'XEM'      , '50.00', '0' ),
        ('assets/bat.png', 'BAT'      , '50.00', '0' ),
        ('assets/agix.png', 'AGIX'    , '50.00', '0' ),
        ('assets/ksm.png', 'KSM'      , '50.00', '0' ),
        ('assets/mask.png', 'MASK'    , '50.00', '0' ),
        ('assets/ht.png', 'HT'        , '50.00', '0' ),
        ('assets/lrc.png', 'LRC'      , '50.00', '0' ),
        ('assets/hot.png', 'HOT'      , '50.00', '0' ),
        ('assets/dash.png', 'DASH'    , '50.00', '0' ),
        ('assets/glmr.png', 'GLMR'    , '50.00', '0' ),
        ('assets/ssv.png', 'SSV'      , '50.00', '0' ),
        ('assets/qtum.png', 'QTUM'    , '50.00', '0' ),
        ('assets/ilv.png', 'ILV'      , '50.00', '0' ),
        ('assets/ray.png', 'RAY'      , '50.00', '0' ),
        ('assets/super.png', 'SUPER'  , '50.00', '0' ),
        ('assets/xch.png', 'XCH'      , '50.00', '0' ),
        ('assets/wld.png', 'WLD'      , '50.00', '0' ),
        ('assets/ethw.png', 'ETHW'    , '50.00', '0' ),
        ('assets/sfp.png', 'SFP'      , '50.00', '0' ),
        ('assets/kda.png', 'KDA'      , '50.00', '0' ),
        ('assets/magic.png', 'MAGIC'  , '50.00', '0' ),
        ('assets/xai.png', 'XAI'      , '50.00', '0' ),
        ('assets/tfuel.png', 'TFUEL'  , '50.00', '0' ),
        ('assets/zrx.png', 'ZRX'      , '50.00', '0' ),
        ('assets/jto.png', 'JTO'      , '50.00', '0' ),
        ('assets/cfg.png', 'CFG'      , '50.00', '0' ),
        ('assets/ant.png', 'ANT'      , '50.00', '0' ),
        ('assets/cvx.png', 'CVX'      , '50.00', '0' ),
        ('assets/mx.png', 'MX'        , '50.00', '0' ),
        ('assets/waves.png', 'WAVES'  , '50.00', '0' ),
        ('assets/jst.png', 'JST'      , '50.00', '0' ),
        ('assets/mobile.png', 'MOBILE', '50.00', '0' ),
        ('assets/rvn.png', 'RVN'      , '50.00', '0' ),
        ('assets/yfi.png', 'YFI'      , '50.00', '0' ),
        ('assets/bico.png', 'BICO'    , '50.00', '0' ),
        ('assets/sushi.png', 'SUSHI'  , '50.00', '0' ),
        ('assets/trac.png', 'TRAC'    , '50.00', '0' ),
        ('assets/ankr.png', 'ANKR'    , '50.00', '0' ),
        ('assets/dcr.png', 'DCR'      , '50.00', '0' ),
        ('assets/meme.png', 'MEME'    , '50.00', '0' ),
        ('assets/ocean.png', 'OCEAN'  , '50.00', '0' ),
        ('assets/rbn.png', 'RBN'      , '50.00', '0' ),
        ('assets/audio.png', 'AUDIO'  , '50.00', '0' ),
        ('assets/storj.png', 'STORJ'  , '50.00', '0' ),
        ('assets/lpt.png', 'LPT'      , '50.00', '0' ),
        ('assets/band.png', 'BAND'    , '50.00', '0' ),
        ('assets/prime.png', 'PRIME'  , '50.00', '0' ),
        ('assets/glm.png', 'GLM'      , '50.00', '0' ),
        ('assets/bal.png', 'BAL'      , '50.00', '0' ),
        ('assets/ont.png', 'ONT'      , '50.00', '0' ),
        ('assets/fnsa.png', 'FNSA'    , '50.00', '0' ),
        ('assets/one.png', 'ONE'      , '50.00', '0' ),
        ('assets/movr.png', 'MOVR'    , '50.00', '0' ),
        ('assets/waxp.png', 'WAXP'    , '50.00', '0' ),
        ('assets/hbar.png', 'HBAR'    , '83.21', '0' ),
        ('assets/imx.png', 'IMX'      , '89.76', '0' ),
        ('assets/sei.png', 'SEI'      , '90.37', '0' ),
        ('assets/rune.png', 'RUNE'    , '89.75', '0' ),
        ('assets/sand.png', 'SAND'    , '93.39', '0' ),
        ('assets/theta.png', 'THETA'  , '91.59', '0' ),
        ('assets/chz.png', 'CHZ'      , '92.30', '0' ),
        ('assets/gala.png', 'GALA'    , '94.59', '0' ),
        ('assets/cake.png', 'CAKE'    , '93.49', '0' ),
        ('assets/frax.png', 'FRAX'    , '91.59', '0' ),
        ('assets/1inch.png', '1INCH'  , '93.07', '0' ),
        ('assets/fet.png', 'FET'      , '91.97', '0' ),
        ('assets/axl.png', 'AXL'      , '92.41', '0' ),
        ('assets/twt.png', 'TWT'      , '92.84', '0' ),
        ('assets/core.png', 'CORE'    , '90.39', '0' ),
        ('assets/enj.png', 'ENJ'      , '92.08', '0' ),
        ('assets/ftn.png', 'FTN'      , '90.45', '0' ),
        ('assets/paxg.png', 'PAXG'    , '93.61', '0' ),
        ('assets/iotx.png', 'IOTX'    , '92.30', '0' ),
        ('assets/trb.png', 'TRB'      , '91.30', '0' ),
        ('assets/floki.png', 'FLOKI'  , '91.93', '0' ),
        ('assets/sxp.png', 'SXP'      , '91.62', '0' ),
        ('assets/sfund.png', 'SFUND'  , '90.11', '0' ),
    ]
    
    symbols = [crypto[1] for crypto in cryptos]
    prices = get_crypto_prices(symbols)
    updated_cryptos = []

    for crypto in cryptos:
        symbol = crypto[1]
        market_cap, price, change_1h, change_24h, change_7d = prices.get(symbol, (None, None, None, None, None))
        rate_ck_class = get_class_for_rate(float(crypto[2]))
        rate_cb_class = get_class_for_rate(float(crypto[3]))
        try:
            change_1h_class = get_class_for_change(change_1h, scale=1)
        except:
            print(crypto)
        change_24h_class = get_class_for_change(change_24h, scale=5)
        change_7d_class = get_class_for_change(change_7d, scale=10)
        updated_cryptos.append(crypto + (price, change_1h, change_24h, change_7d, market_cap, rate_ck_class, rate_cb_class, change_24h_class, change_1h_class, change_7d_class))


    if column and order:
        reverse_order = True if order == 'desc' else False

        def get_sort_key(crypto, col):
            """Helper function to get the correct sort key based on column."""
            column_keys = {
                'rate_ck': 2, 'rate_cb': 3, 'price': 4, 'change_1h': 5, 'change_24h': 6,
                'change_7d': 7, 'market_cap': 8
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