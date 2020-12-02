from qttp.tools.log import setup_custom_logger
import ccxt

logger = setup_custom_logger("Apis")

def exception_handler(func):
    def inner_function(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            done_message = (
                f"{args[0].api}, {args[0].market}, "
                f"{func.__name__.upper()} Method Execute"
            )
            logger.info(done_message)
            return result
        except (ccxt.NetworkError, ccxt.InsufficientFunds, IndexError) as e:
            error_message = (
                        f"{args[0].api}, {args[0].market}, "
                        f"{func.__name__.upper()}, {type(e).__name__}"
                    )
            logger.info(error_message)
    return inner_function

class Apis:
    def __init__(self, access, secret, market):
        self.api.apiKey = access
        self.api.secret = secret
        self.market = market

    @exception_handler
    def limit_buy(self, amount, price):
        buy = self.api.create_order(symbol=self.market, type="limit",
                                    side="buy", amount=amount, price=price)
        return buy

    @exception_handler
    def limit_sell(self, amount, price):
        sell = self.api.create_order(symbol=self.market, type="limit",
                                    side="sell", amount=amount, price=price)
        return sell

    @exception_handler
    def market_buy(self, amount, price=None):
        buy = self.api.create_order(symbol=self.market, type="market",
                                    side="buy", amount=amount, price=price)
        return buy

    @exception_handler
    def market_sell(self, amount, price=None):
        sell = self.api.create_order(symbol=self.market, type="market",
                                    side="sell", amount=amount, price=price)
        return sell

    @exception_handler
    def ask_price(self, num):
        market = self.__market_name_change()
        return self.api.fetchOrderBook(market)['asks'][0][num]

    @exception_handler
    def bid_price(self, num):
        market = self.__market_name_change()
        return self.api.fetchOrderBook(market)['bids'][0][num]

    @exception_handler
    def ask_prices(self):
        market = self.__market_name_change()
        return self.api.fetchOrderBook(market, limit=100)['asks']

    @exception_handler
    def bid_prices(self):
        market = self.__market_name_change()
        return self.api.fetchOrderBook(market, limit=100)['bids']

    def __market_name_change(self):
        if self.market.startswith("KRW-"):
            market = self.market[-3:] + "/" + self.market[:3]
        else:
            market = self.market
        return market

class DeribitApi(Apis):
    def __init__(self, *args, **kwargs):
        self.api = ccxt.deribit()
        super().__init__(*args, **kwargs)
        instrument_name = {'instrument_name' : self.market,}
        currency = {'currency' : self.market[:3]}
        self.position = self.api.private_get_get_position(instrument_name)
        self.account = self.api.private_get_get_account_summary(currency)

    @exception_handler
    def cancel_all(self):
        self.api.cancel_all_orders()

    @exception_handler
    def avg_price(self):
        avg_price = self.position['result']['average_price']
        return avg_price

    @exception_handler
    def size(self):
        size = self.position['result']['size']
        return size

    @exception_handler
    def equity(self):
        return self.account['result']['equity']


class UpbitApi(Apis):
    def __init__(self, *args, **kwargs):
        self.api = ccxt.upbit()
        super().__init__(*args, **kwargs)
        self.__account()

    @exception_handler
    def avg_price(self):
        return self.u_avg_price

    @exception_handler
    def size(self):
        return self.u_size

    @exception_handler
    def equity(self):
        return self.u_equity_total

    @exception_handler
    def cancel_all(self):
        order_ids = self.__order_ids()
        for order_id in order_ids:
            self.api.cancel_order(order_id)

    def __order_ids(self):
        try:
            orders = self.api.fetchOpenOrders()
            order_ids = [order['info']['uuid'] for order in orders]

        except IndexError as e:
            order_ids = []

        return order_ids

    def __account(self):
        account = self.api.private_get_accounts()

        u_equity_total = 0
        u_avg_price = 0
        u_size = 0

        for equity in account:
            if equity['currency'] == 'KRW':
                u_equity_total = u_equity_total + float(equity['locked'])
                u_equity_total = u_equity_total + float(equity['balance'])
            else:
                avg_buy = float(equity["avg_buy_price"])
                balance = float(equity['balance'])
                u_equity_total = u_equity_total + (avg_buy * balance)

            if equity['currency'] == self.market[-3:]:
                u_avg_price = equity["avg_buy_price"]
                u_size = equity["balance"]

        self.u_equity_total = u_equity_total
        self.u_avg_price = u_avg_price
        self.u_size = u_size
