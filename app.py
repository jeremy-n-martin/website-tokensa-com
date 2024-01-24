import requests
import os
import logging
from flask import Flask, render_template, request

app = Flask(__name__)

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

    print("a")

    #rajouter une colonne avec les cotes binance etc
    #rajouter une colonne avec les layer etc
    #rajouter une colonne avec les dates de création etc
    #rajouter une colonne liquidity Volume/Market cap (24h)
    cryptos = [
        ('assets/btc.png', 'BTC', '96', '95', '00'),
        ('assets/eth.png', 'ETH', '96', '96', '82'),
        ('assets/bnb.png', 'BNB', '92', '93', '77'),
        ('assets/sol.png', 'SOL', '91', '97', '62'),
        ('assets/xrp.png', 'XRP', '94', '95', '68'),
        ('assets/ada.png', 'ADA', '89', '95', '65'),
        ('assets/avax.png', 'AVAX', '94', '97', '71'),
        ('assets/doge.png', 'DOGE', '86', '97', '00'),
        ('assets/trx.png', 'TRX', '88', '90', '61'),
        ('assets/link.png', 'LINK', '87', '94', '00'),
        ('assets/dot.png', 'DOT', '83', '96', '70'),
        ('assets/ton.png', 'TON', '93', '96', '63'),
        ('assets/matic.png', 'MATIC', '93', '96', '70'),
        ('assets/shib.png', 'SHIB', '91', '92', '00'),
        ('assets/ltc.png', 'LTC', '77', '88', '56'),
        ('assets/icp.png', 'ICP', '81', '97', '00'),
        ('assets/bch.png', 'BCH', '74', '88', '53'),
        ('assets/uni.png', 'UNI', '94', '95', '75'),
        ('assets/atom.png', 'ATOM', '94', '88', '71'),
        ('assets/leo.png', 'LEO', '86', '88', '54'),
        ('assets/etc.png', 'ETC', '77', '88', '57'),
        ('assets/xlm.png', 'XLM', '85', '89', '63'),
        ('assets/okb.png', 'OKB', '92', '97', '67'),
        ('assets/inj.png', 'INJ', '84', '97', '00'),
        ('assets/op.png', 'OP', '88', '94', '62'),
        ('assets/near.png', 'NEAR', '90', '88', '70'),
        ('assets/apt.png', 'APT', '94', '97', '63'),
        ('assets/tia.png', 'TIA', '69', '97', '57'),
        ('assets/xmr.png', 'XMR', '73', '88', '63'),
        ('assets/ldo.png', 'LDO', '91', '96', '00'),
        ('assets/fil.png', 'FIL', '79', '89', '67'),
        ('assets/hbar.png', 'HBAR', '83', '90', '66'),
        ('assets/imx.png', 'IMX', '89', '95', '00'),
        ('assets/arb.png', 'ARB', '94', '89', '57'),
        ('assets/kas.png', 'KAS', '00', '00', '00'),
        ('assets/mnt.png', 'MNT', '81', '93', '00'),
        ('assets/stx.png', 'STX', '78', '88', '76'),
        ('assets/cro.png', 'CRO', '92', '88', '63'),
        ('assets/vet.png', 'VET', '92', '97', '64'),
        ('assets/mkr.png', 'MKR', '91', '90', '00'),
        ('assets/sei.png', 'SEI', '90', '96', '00'),
        ('assets/rndr.png', 'RNDR', '59', '97', '49'),
        ('assets/ordi.png', 'ORDI', '52', '00', '00'),
        ('assets/bsv.png', 'BSV', '70', '00', '00'),
        ('assets/grt.png', 'GRT', '00', '97', '68'),
        ('assets/algo.png', 'ALGO', '87', '97', '67'),
        ('assets/aave.png', 'AAVE', '85', '91', '69'),
        ('assets/rune.png', 'RUNE', '89', '00', '00'),
        ('assets/qnt.png', 'QNT', '77', '84', '54'),
        ('assets/egld.png', 'EGLD', '90', '95', '00'),
        ('assets/sui.png', 'SUI', '83', '95', '60'),
        ('assets/mina.png', 'MINA', '73', '97', '64'),
        ('assets/sats.png', '1000SATS', '56', '00', '00'),
        ('assets/flow.png', 'FLOW', '79', '91', '67'),
        ('assets/hnt.png', 'HNT', '73', '97', '66'),
        ('assets/ftm.png', 'FTM', '89', '97', '66'),
        ('assets/snx.png', 'SNX', '84', '96', '00'),
        ('assets/sand.png', 'SAND', '93', '97', '68'),
        ('assets/axs.png', 'AXS', '85', '92', '66'),
        ('assets/xtz.png', 'XTZ', '86', '84', '00'),
        ('assets/theta.png', 'THETA', '91', '84', '00'),
        ('assets/kcs.png', 'KCS', '76', '89', '00'),
        ('assets/btt.png', 'BTT', '78', '93', '00'),
        ('assets/beam.png', 'BEAM', '67', '84', '00'),
        ('assets/astr.png', 'ASTR', '83', '97', '00'),
        ('assets/wemix.png', 'WEMIX', '93', '00', '00'),
        ('assets/dydx.png', 'ETHDYDX', '44', '85', '00'),
        ('assets/ftt.png', 'FTT', '67', '00', '00'),
        ('assets/mana.png', 'MANA', '85', '88', '66'),
        ('assets/bgb.png', 'BGB', '75', '91', '00'),
        ('assets/blur.png', 'BLUR', '71', '94', '00'),
        ('assets/neo.png', 'NEO', '73', '94', '59'),
        ('assets/osmo.png', 'OSMO', '00', '00', '00'),
        ('assets/chz.png', 'CHZ', '92', '97', '00'),
        ('assets/eos.png', 'EOS', '82', '89', '59'),
        ('assets/flr.png', 'FLR', '73', '88', '55'),
        ('assets/kava.png', 'KAVA', '86', '00', '00'),
        ('assets/bonk.png', 'BONK', '60', '85', '00'),
        ('assets/woo.png', 'WOO', '86', '95', '00'),
        ('assets/iota.png', 'IOTA', '73', '90', '60'),
        ('assets/klay.png', 'KLAY', '85', '96', '00'),
        ('assets/cfx.png', 'CFX', '71', '89', '59'),
        ('assets/xdc.png', 'XDC', '52', '00', '51'),
        ('assets/rose.png', 'ROSE', '79', '91', '00'),
        ('assets/cake.png', 'CAKE', '94', '93', '00'),
        ('assets/fxs.png', 'FXS', '81', '94', '00'),
        ('assets/gala.png', 'GALA', '94', '84', '58'),
        ('assets/xec.png', 'XEC', '71', '90', '00'),
        ('assets/ar.png', 'AR', '69', '91', '00'),
        ('assets/lunc.png', 'LUNC', '49', '00', '00'),
        ('assets/sc.png', 'SC', '67', '92', '00'),
        ('assets/rpl.png', 'RPL', '77', '93', '54'),
        ('assets/akt.png', 'AKT', '74', '94', '00'),
        ('assets/ens.png', 'ENS', '85', '93', '00'),
        ('assets/ron.png', 'RON', '86', '92', '00'),
        ('assets/manta.png', 'MANTA', '71', '92', '00'),
        ('assets/crv.png', 'CRV', '66', '92', '66'),
        ('assets/gno.png', 'GNO', '77', '87', '00'),
        ('assets/fet.png', 'FET', '91', '77', '54'),
        ('assets/pendle.png', 'PENDLE', '81', '83', '65'),
        ('assets/cspr.png', 'CSPR', '80', '92', '00'),
        ('assets/ape.png', 'APE', '93', '92', '60'),
        ('assets/axl.png', 'AXL', '92', '84', '54'),
        ('assets/nexo.png', 'NEXO', '77', '92', '00'),
        ('assets/gt.png', 'GT', '87', '76', '00'),
        ('assets/pyth.png', 'PYTH', '89', '92', '00'),
        ('assets/gmt.png', 'GMT', '76', '92', '00'),
        ('assets/pepe.png', 'PEPE', '87', '90', '00'),
        ('assets/1inch.png', '1INCH', '93', '92', '00'),
        ('assets/xrd.png', 'XRD', '73', '92', '00'),
        ('assets/uma.png', 'UMA', '73', '92', '00'),
        ('assets/twt.png', 'TWT', '93', '92', '68'),
        ('assets/comp.png', 'COMP', '86', '50', '50'),
        ('assets/core.png', 'CORE', '90', '83', '00'),
        ('assets/gmx.png', 'GMX', '91', '90', '64'),
        ('assets/gas.png', 'GAS', '60', '92', '00'),
        ('assets/paxg.png', 'PAXG', '93', '92', '00'),
        ('assets/nft.png', 'NFT', '61', '78', '49'),
        ('assets/xem.png', 'XEM', '61', '00', '00'),
        ('assets/luna.png', 'LUNA', '59', '92', '00'),
        ('assets/metis.png', 'METIS', '58', '90', '00'),
        ('assets/elf.png', 'ELF', '70', '92', '00'),
        ('assets/btg.png', 'BTG', '46', '00', '00'),
        ('assets/skl.png', 'SKL', '85', '92', '00'),
        ('assets/enj.png', 'ENJ', '92', '92', '65'),
        ('assets/iotx.png', 'IOTX', '92', '92', '00'),
        ('assets/zec.png', 'ZEC', '73', '82', '00'),
        ('assets/zil.png', 'ZIL', '80', '92', '00'),
        ('assets/wif.png', 'WIF', '00', '00', '00'),
        ('assets/celo.png', 'CELO', '73', '92', '00'),
        ('assets/deso.png', 'DESO', '72', '84', '00'),
        ('assets/ht.png', 'HT', '79', '87', '55'),
        ('assets/ntrn.png', 'NTRN', '67', '88', '00'),
        ('assets/bat.png', 'BAT', '91', '85', '00'),
        ('assets/mask.png', 'MASK', '00', '92', '57'),
        ('assets/agix.png', 'AGIX', '81', '92', '63'),
        ('assets/ksm.png', 'KSM', '72', '85', '00'),
        ('assets/trb.png', 'TRB', '91', '78', '55'),
        ('assets/hot.png', 'HOT', '00', '00', '00'),
        ('assets/lrc.png', 'LRC', '85', '00', '00'),
        ('assets/dash.png', 'DASH', '73', '89', '00'),
        ('assets/qtum.png', 'QTUM', '73', '92', '00'),
        ('assets/xch.png', 'XCH', '72', '92', '00'),
        ('assets/ilv.png', 'ILV', '78', '92', '00'),
        ('assets/ethw.png', 'ETHW', '70', '76', '00'),
        ('assets/glmr.png', 'GLMR', '80', '92', '00'),
        ('assets/ssv.png', 'SSV', '69', '92', '54'),
        ('assets/super.png', 'SUPER', '82', '92', '00'),
        ('assets/sfp.png', 'SFP', '91', '85', '50'),
        ('assets/tfuel.png', 'TFUEL', '72', '91', '00'),
        ('assets/ray.png', 'RAY', '72', '00', '00'),
        ('assets/t.png', 'T', '85', '85', '00'),
        ('assets/wld.png', 'WLD', '82', '89', '00'),
        ('assets/kda.png', 'KDA', '00', '00', '00'),
        ('assets/jto.png', 'JTO', '69', '69', '00'),
        ('assets/magic.png', 'MAGIC', '78', '86', '53'),
        ('assets/floki.png', 'FLOKI', '91', '92', '00'),
        ('assets/ant.png', 'ANT', '76', '89', '55'),
        ('assets/mx.png', 'MX', '77', '85', '55'),
        ('assets/cvx.png', 'CVX', '86', '85', '53'),
        ('assets/cfg.png', 'CFG', '81', '00', '00'),
        ('assets/zrx.png', 'ZRX', '83', '00', '00'),
        ('assets/waves.png', 'WAVES', '73', '83', '00'),
        ('assets/jst.png', 'JST', '75', '00', '00'),
        ('assets/rbn.png', 'RBN', '70', '89', '00'),
        ('assets/rvn.png', 'RVN', '72', '90', '00'),
        ('assets/yfi.png', 'YFI', '69', '92', '63'),
        ('assets/trac.png', 'TRAC', '70', '91', '53'),
        ('assets/sushi.png', 'SUSHI', '82', '92', '60'),
        ('assets/jasmy.png', 'JASMY', '83', '82', '00'),
        ('assets/dcr.png', 'DCR', '67', '87', '00'),
        ('assets/ankr.png', 'ANKR', '87', '88', '62'),
        ('assets/xai.png', 'XAI', '00', '50', '50'),
        ('assets/ocean.png', 'OCEAN', '89', '91', '62'),
        ('assets/bico.png', 'BICO', '78', '90', '54'),
        ('assets/mobile.png', 'MOBILE', '66', '50', '50'),
        ('assets/icx.png', 'ICX', '81', '89', '00'),
        ('assets/storj.png', 'STORJ', '87', '81', '00'),
        ('assets/audio.png', 'AUDIO', '72', '92', '00'),
        ('assets/glm.png', 'GLM', '76', '92', '00'),
        ('assets/lpt.png', 'LPT', '78', '88', '00'),
        ('assets/bal.png', 'BAL', '68', '00', '00'),
        ('assets/band.png', 'BAND', '88', '90', '60'),
        ('assets/meme.png', 'MEME', '89', '87', '00'),
        ('assets/movr.png', 'MOVR', '70', '80', '00'),
        ('assets/ont.png', 'ONT', '79', '92', '00'),
        ('assets/fnsa.png', 'FNSA', '89', '83', '00'),
        ('assets/sxp.png', 'SXP', '91', '00', '00'),
        ('assets/waxp.png', 'WAXP', '81', '91', '00'),
        ('assets/hex.png', 'HEX', '00', '00', '00'),
        ('assets/tao.png', 'TAO', '59', '90', '00'),
        ('assets/cheel.png', 'CHEEL', '89', '92', '53'),
        ('assets/frax.png', 'FRAX', '91', '92', '60'),
        ('assets/pokt.png', 'POKT', '00', '89', '00'),
        ('assets/kuji.png', 'KUJI', '79', '74', '00'),
        ('assets/rlb.png', 'RLB', '00', '00', '00'),
        ('assets/lyx.png', 'LYX', '00', '00', '00'),
        ('assets/flex.png', 'FLEX', '88', '75', '00'),
        ('assets/azero.png', 'AZERO', '73', '92', '00'),
        ('assets/strd.png', 'STRD', '00', '77', '56'),
        ('assets/orbr.png', 'ORBR', '48', '77', '37'),
        ('assets/one.png', 'ONE', '77', '92', '00'),
        ('assets/ftn.png', 'FTN', '90', '83', '52'),
        ('assets/prime.png', 'PRIME', '70', '92', '00'),
        ('assets/ctsi.png', 'CTSI', '92', '92', '53'),
        ('assets/sfund.png', 'SFUND', '90', '00', '00'),
    ]
    
    symbols = [crypto[1] for crypto in cryptos]
    prices = get_crypto_prices(symbols)
    updated_cryptos = []

    for crypto in cryptos:
        symbol = crypto[1]
        market_cap, price, change_1h, change_24h, change_7d = prices.get(symbol, (None, None, None, None, None))
        rate_ck_class = get_class_for_rate_ck(float(crypto[2]))
        rate_cb_class = get_class_for_rate_cb(float(crypto[3]))
        rate_ti_class = get_class_for_rate_ti(float(crypto[4]))

        change_1h_class = get_class_for_change(change_1h, scale=1)
        change_24h_class = get_class_for_change(change_24h, scale=5)
        change_7d_class = get_class_for_change(change_7d, scale=10)
        updated_cryptos.append(crypto + (price, change_1h, change_24h, change_7d, market_cap,
                                         rate_ck_class, rate_cb_class, rate_ti_class, change_24h_class,
                                         change_1h_class, change_7d_class))


    if column and order:
        reverse_order = True if order == 'desc' else False

        def get_sort_key(crypto, col):
            """Helper function to get the correct sort key based on column."""
            column_keys = {
                'rate_ck': 2, 'rate_cb': 3, 'rate_ti': 4, 'price': 5, 'change_1h': 6,
                'change_24h': 7, 'change_7d': 8, 'market_cap': 9
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