# Import Built-ins
import logging

# Import Third-Party

# Import Homebrew
from bitex.formatters.base import Formatter


log = logging.getLogger(__name__)


class HitBtcFormatter(Formatter):
    @staticmethod
    def order_book(data, *args, **kwargs):
        print('formatter: order_book')
        ret = {'asks': [], 'bids': []}
        for i in data['ask']: ret['asks'].append([i['price'], i['size']])
        for i in data['bid']: ret['bids'].append([i['price'], i['size']])
        try:
            return ret
        except KeyError:
            return False

    @staticmethod
    def pairs(data, *args, **kwargs):
        ret = []
        for i in data:
            ret.append(i['id'])
        return ret
