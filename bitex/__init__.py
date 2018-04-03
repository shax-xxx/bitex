import logging
logging.getLogger(__name__).warning("The API clients available in this package are deprecated "
                                    "and will be no longer available in their current form "
                                    "starting with version 2.0!")
from .interfaces import Kraken, Bitfinex, Bitstamp, CCEX, Coincheck
from .interfaces import Cryptopia, Gemini, ItBit, OKCoin, RockTradingLtd
from .interfaces import Yunbi, Bittrex, Poloniex, Quoine, QuadrigaCX
from .interfaces import Vaultoro, HitBtc, Bter, GDAX
from ._version import __version__
version=__version__
