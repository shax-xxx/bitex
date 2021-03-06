# Import Built-Ins
import logging

# Import Third-Party

# Import Homebrew
from ..formatters.base import Formatter

# Init Logging Facilities
log = logging.getLogger(__name__)


class BtstFormatter(Formatter):

    @staticmethod
    def ticker(data, *args, **kwargs):
        return (data['bid'], data['ask'], data['high'], data['low'], data['open'],
                None, data['last'], data['volume'], data['timestamp'])


