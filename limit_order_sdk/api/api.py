from typing import Any, Dict, Union, Optional, List
from urllib.parse import urlencode
from limit_order_sdk.api import ApiConfig, LimitOrderApiItem, StatusKey, SortKey, DEV_PORTAL_LIMIT_ORDER_BASE_URL, Pager
from limit_order_sdk.api.connector import HttpProviderConnector
from limit_order_sdk.limit_order import LimitOrder
from limit_order_sdk.address import Address


class Api:
    def __init__(self, config: ApiConfig):
        self.base_url: str = config.base_url or DEV_PORTAL_LIMIT_ORDER_BASE_URL
        self.chain_id: int = config.chain_id
        self.http_client: HttpProviderConnector = config.http_connector
        self.auth_header: str = f"Bearer {config.auth_key}"

    def submit_order(self, order: LimitOrder, signature: str) -> None:
        """
        Submit order to orderbook
        @param order
        @param signature
        """
        self.http_client.post(
            self.url("/"),
            {"orderHash": order.get_order_hash(self.chain_id), "signature": signature, "data": {**(order.build().__dict__), "extension": order.extension.encode()}},
            self.headers(),
        )

    def get_orders_by_maker(self, maker: Address, filters: Optional[Dict[str, Any]] = None, sort_key: Optional[SortKey] = None) -> LimitOrderApiItem:
        """
        Fetch orders created by `maker`
        """
        params: Dict[str, Any] = {"limit": None, "page": None, "statuses": None, "makerAsset": None, "takerAsset": None, "sortBy": "createdAt"}
        if filters:
            params.update(filters)
        return self.http_client.get(self.url(f"/address/{maker}", params), self.headers())

    def get_order_by_hash(self, hash: str) -> LimitOrderApiItem:
        """
        Get limit order by hash
        Error will be thrown if order is not found
        """
        return self.http_client.get(self.url(f"/order/{hash}"), self.headers())

    def url(self, path: str, params: Optional[Dict[str, str]] = None):
        if params:
            filtered_params = {k: v for k, v in params.items() if v is not None}
            query = f"?{urlencode(filtered_params)}"
        else:
            query = ""
        return f"{self.base_url}/{self.chain_id}{path}{query}"

    def headers(self, additional: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        if additional is None:
            return {"Authorization": self.auth_header}
        else:
            return {"Authorization": self.auth_header, **additional}
