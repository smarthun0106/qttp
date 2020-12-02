from qttp.trading_candles import DeribitCandle
from qttp.trading_forms import DeribitForm
from qttp.trading_self import DeribitApi
from qttp.trading_self import UpbitApi

def trading_candles_test():
    candles = DeribitCandle("BTC-PERPETUAL").real_time_candle_days()
    print(candles)

def trading_forms_test():
    pass

def trading_self_deribit_test():
    KD_001_BTC_KEY = "E1qbcbs1"
    KD_001_BTC_SECRET = "CWp6jruam9s8mJvgjMFqhZZNGAub76QA-TxYdHFkgg0"
    access          = KD_001_BTC_KEY
    secret          = KD_001_BTC_SECRET
    market          = 'BTC-PERPETUAL'

    trading = DeribitApi(access, secret, market)
    # buy = trading.limit_buy(amount=30, price=18000)
    # sell = trading.limit_sell(amount=30, price=20000)
    # market_buy = trading.market_buy(amount=10)
    # market_sell = trading.market_sell(amount=10)
    # print(market_sell)
    # trading.cancel_all()
    print(trading.ask_price(0))
    # print(trading.bid_price(0))
    # print(trading.avg_price())
    # print(trading.size())
    # print(trading.equity())

def trading_self_upbit_test():

    TAEHUN_UPBIT_ACCESS_KEY = "lpeP99y29PyxHNoxBpicfe5VP6dVlpORPyAP7xeV"
    TAEHUN_UPBIT_SECRET_KEY = "ST4sIxEjaXx9Nhz3eUUEInIZWCY103WxkfipiyqR"
    access          = TAEHUN_UPBIT_ACCESS_KEY
    secret          = TAEHUN_UPBIT_SECRET_KEY
    market          = "KRW-BTC"
    trading = UpbitApi(access, secret, market)
    # buy = trading.limit_buy(amount=0.0001, price=19500000)
    # sell = trading.limit_sell(amount=0.0001, price=19500000)
    # market_buy = trading.market_buy(amount=0.0001, price=100) # upbit market buy need price to calculate amount
    # market_sell = trading.market_sell(amount=10)
    # trading.cancel_all()
    # print(trading.ask_price(0))
    # print(trading.bid_price(0))
    # print(trading.avg_price())
    # print(trading.size())
    # print(trading.equity())
    print(trading.ask_price(0))


trading_self_deribit_test()
# trading_self_upbit_test()
