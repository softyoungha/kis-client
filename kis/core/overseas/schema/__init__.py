from pydantic import BaseModel

from .balance_schema import *
from .order_schema import *
from .quote_schema import *


class Currency(BaseModel):
    price: float  # 현가
    opening: float  # 시가
    change: float  # 전일대비
    buying: float  # 살때
    selling: float  # 팔때
    sending: float  # 보낼때
    receiving: float  # 받을 때
