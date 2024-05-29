from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Union, Optional, List
from limit_order_sdk.api.connector import HttpProviderConnector
from limit_order_sdk.limit_order import LimitOrderV4Struct


@dataclass
class ApiConfig:
    auth_key: str
    http_connector: HttpProviderConnector
    chain_id: int
    base_url: Optional[str] = None


@dataclass
class LimitOrderApiItem:
    signature: str
    order_hash: str
    create_date_time: str
    remaining_maker_amount: str
    maker_balance: str
    maker_allowance: str
    data: Union[LimitOrderV4Struct, Any]
    maker_rate: str
    taker_rate: str
    is_maker_contract: str
    order_invalid_reason: Optional[List[str]]


class StatusKey(Enum):
    """
    1 - Valid orders,
    2 - Temporarily invalid orders,
    3 - Invalid orders.
    """

    VALID = 1
    TEMP_INVALID = 2
    INVALID = 3


class SortKey(Enum):
    CREATE_DATE_TIME = "createDateTime"
    TAKER_RATE = "takerRate"
    MAKER_RATE = "makerRate"
    MAKER_AMOUNT = "makerAmount"
    TAKER_AMOUNT = "takerAmount"
