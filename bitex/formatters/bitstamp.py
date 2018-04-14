"""FormattedResponse Class for Standardized methods of the Bitstamp Interface class."""
# Import Built-ins
import time
from datetime import datetime

# Import Home-brewed
from bitex.formatters.base import APIResponse


class BitstampFormattedResponse(APIResponse):
    """FormattedResponse class.

    Returns the standardized method's json results as a formatted data in a namedTuple.
    """

    def ticker(self):
        """Return namedtuple with given data."""
        data = self.json(parse_int=str, parse_float=str)

        bid = data["bid"]
        ask = data["ask"]
        high = data["high"]
        low = data["low"]
        last = data["last"]
        volume = data["volume"]
        timestamp = datetime.utcfromtimestamp(float(data["timestamp"]))
        return super(BitstampFormattedResponse, self).ticker(bid, ask, high, low, last, volume,
                                                             timestamp)

    def order_book(self):
        """Return namedtuple with given data."""
        data = self.json()
        asks = []
        bids = []
        for i in data['asks']:
            asks.append([float(i[0]), float(i[1])])
        for i in data['bids']:
            bids.append([float(i[0]), float(i[1])])

        return super(BitstampFormattedResponse, self).order_book(bids, asks, int(data['timestamp']))

    def trades(self):
        """Return namedtuple with given data."""
        data = self.json()
        tradelst = []
        timestamp = datetime.utcnow()
        for trade in data:
            tradelst.append({'id':trade['tid'],'price':trade['price'],'qty':trade['amount'],
                             'time':int(time.time()*1000),'isBuyerMaker':trade['type']=='0','isBestMatch':None})
            # what meaning isBuyerMaker is? if we should remain it in all trades formatter?
            # raise NotImplementedError
        return super(BitstampFormattedResponse, self).trades(tradelst, timestamp)

    def bid(self):
        """Return namedtuple with given data."""
        data = self.json(parse_int=str, parse_float=str)
        oid, ts, side = data['id'], data['datetime'], 'ask' if data['type'] else 'bid'
        price, size = data['price'], data['amount']
        return super(BitstampFormattedResponse, self).bid(oid, price, size, side, 'N/A', ts)

    def ask(self):
        """Return namedtuple with given data."""
        data = self.json(parse_int=str, parse_float=str)
        oid, ts, side = data['id'], data['datetime'], 'ask' if data['type'] else 'bid'
        price, size = data['price'], data['amount']
        return super(BitstampFormattedResponse, self).ask(oid, price, size, side, 'N/A', ts)

    def order_status(self):
        """Return namedtuple with given data."""
        data = self.json(parse_int=str, parse_float=str)
        state = data['status']
        # oid = self.method_args[0]
        oid = data['id']
        ts = self.received_at
        return super(BitstampFormattedResponse, self).order_status(
            oid, 'N/A', 'N/A', 'N/A', 'N/A', state, ts)

    def cancel_order(self):
        """Return namedtuple with given data."""
        data = self.json(parse_int=str, parse_float=float)
        if 'error' in data:
            extracted_data=(0, False, None, data['error'])
        else:
            extracted_data = (data['id'], 'ask' if data['type']=='1' else 'bid')

        return super(BitstampFormattedResponse, self).cancel_order(*extracted_data)

    def open_orders(self):
        """Return namedtuple with given data."""
        data = self.json(parse_int=str, parse_float=str)
        unpacked_orders = []
        for order in data:
            if order['type'] == '1':
                side = 'ask'
            else:
                side = 'bid'
            if 'pair' in self.method_kwargs:
                unpacked_order = (order['id'], self.method_kwargs['pair'], order['price'],
                                  order['amount'], side, order['datetime'])
            else:
                unpacked_order = (order['id'], order['currency_pair'], order['price'], order['amount'],
                                  side, order['datetime'])
            unpacked_orders.append(unpacked_order)

        ts = self.received_at
        return super(BitstampFormattedResponse, self).open_orders(unpacked_orders, ts)

    def wallet(self):
        """Return namedtuple with given data."""
        data = self.json(parse_int=str, parse_float=str)
        balances = {}
        for i in data:
            if i[-10:] == '_available':
                available = float(data[i])
                if available > 0:
                    balances[i[:-10].upper()] = data[i]
        return super(BitstampFormattedResponse, self).wallet(balances, self.received_at)
