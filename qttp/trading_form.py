import ccxt
from pprint import pprint

class Forms:
    def __init__(self, *args, **kwargs):
        self.api.apiKey = access
        self.api.secret = secret
        self.market = market

    def form_01(self, ase):
        print(ase)

    def __signal(self):
        signal = self.strategy(self.df).iloc[-1, -2]
        return signal

    def __cancel(self):
        order_ids = self.__order_ids()
        for order_id in order_ids:
            self.api.cancel_order(order_id)

    def __order_ids(self):
        try:
            orders = self.api.fetchOpenOrders()
            order_ids = [order['info']['order_id'] for order in orders]

        except IndexError as e:
            order_ids = []
        return order_ids


class Deribit(Forms):
    def __init__(self, *args, **kwargs):
        self.api = ccxt.deribit()
        super().__init__(*args, **kwargs)
        instrument_name = {'instrument_name' : self.market,}
        currency = {'currency' : self.market[:3]}
        self.position = self.api.private_get_get_position(instrument_name)
        self.account = self.api.private_get_get_account_summary(currency)

    def form_01(self):
        ase = {
            "market" : self.market,
            "avg_price" : self.__avg_price(),
            "size" : self.__size(),
            "equity" : self.__equity()
        }
        super().form_01(ase)

    def __avg_price(self):
        avg_price = self.position['result']['average_price']
        return avg_price

    def __size(self):
        size = self.position['result']['size']
        return size

    def __equity(self):
        return self.account['result']['equity']


class Upbit(Forms):
    def __init__(self, *args, **kwargs):
        self.api = ccxt.upbit()
        super().__init__(*args, **kwargs)
        self.account = self.api.private_get_accounts()

    def form_01(self):
        ase = {
            "market" : self.market,
            "avg_price" : self.__avg_price(),
            "size" : self.__size(),
            "equity" : self.__equity()
        }
        super().form_01(ase)

    def __avg_price(self):
        avg_price = self.__filter("position")
        return avg_price

    def __size(self):
        size = self.__filter("size")
        return size

    def __equity(self):
        equtiy = self.__filter("equity")
        return equtiy

    def __filter(self, option):
        equity_total = 0
        position = 0
        size = 0
        for equity in self.account:
            if equity['currency'] == 'KRW':
                equity_total = equity_total + float(equity['locked'])
                equity_total = equity_total + float(equity['balance'])
            else:
                avg_buy = float(equity["avg_buy_price"])
                balance = float(equity['balance'])
                equity_total = equity_total + (avg_buy * balance)

            if equity['currency'] == self.market[-3:]:
                position = equity["avg_buy_price"]
                size = equity["balance"]


        if option == "position":
            return position

        if option == "size":
            return size

        if option == "equity":
            return equity_total

class Coinbase(Forms):
    def __init__(self, *args, **kwargs):
        self.api = ccxt.coinbase()
        super().__init__(*args, **kwargs)
        self.account = self.api.private_get_accounts()



if __name__ == "__main__":

    coinbase_key = "rQXJ3iFInU1z7K2R"
    coinbase_secret = "VLMNaNvQlPAPZEJR0QdFNDZaxFqdzotF"

    KD_001_BTC_KEY = "E1qbcbs1"
    KD_001_BTC_SECRET = "CWp6jruam9s8mJvgjMFqhZZNGAub76QA-TxYdHFkgg0"

    TAEHUN_UPBIT_ACCESS_KEY = "lpeP99y29PyxHNoxBpicfe5VP6dVlpORPyAP7xeV"
    TAEHUN_UPBIT_SECRET_KEY = "ST4sIxEjaXx9Nhz3eUUEInIZWCY103WxkfipiyqR"

    access          = KD_001_BTC_KEY

    secret          = KD_001_BTC_SECRET



    market          = 'BTC-PERPETUAL'

    ratio_to_invest = 0.20

    strategy        = 'a'

    df              = 'b'

    trading = Deribit(access, secret, market,
                    ratio_to_invest, strategy, df)

    trading.form_01()

    # KD_001_BTC_KEY = "E1qbcbs1"
    # KD_001_BTC_SECRET = "CWp6jruam9s8mJvgjMFqhZZNGAub76QA-TxYdHFkgg0"
    #
    #
    # access          = KD_001_BTC_KEY
    #
    # secret          = KD_001_BTC_SECRET
    #
    # market          = 'BTC-PERPETUAL'
    #
    # ratio_to_invest = 0.20
    #
    # strategy        = 'a'
    #
    # df              = 'b'
    #
    # trading = Deribit(access, secret, market,
    #                   ratio_to_invest, strategy, df)
    # trading.equity()
