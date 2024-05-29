import requests
from typing import Any, Dict
from limit_order_sdk.api.connector.http import HttpProviderConnector
from limit_order_sdk.api.errors import AuthError


class FetchProviderConnector(HttpProviderConnector):
    def get(self, url: str, headers: Dict[str, str]) -> Any:
        """
        Sends a GET request to the specified URL with the provided headers.

        Raises:
            AuthError: If the response has a status code of 401.
            Exception: For other unsuccessful status codes.
        """
        response = requests.get(url, headers=headers)
        if response.status_code == 401:
            raise AuthError("Authorization failed")
        response.raise_for_status()  # This will raise an exception for HTTP error codes
        return response.json()

    def post(self, url: str, data: Dict[str, Any], headers: Dict[str, str]) -> Any:
        """
        Sends a POST request to the specified URL with the provided data and headers.

        Raises:
            AuthError: If the response has a status code of 401.
            Exception: For other unsuccessful status codes.
        """
        headers.update({"Content-Type": "application/json"})
        response = requests.post(url, json=data, headers=headers)
        if response.status_code == 401:
            raise AuthError("Authorization failed")
        response.raise_for_status()
        return response.json()
