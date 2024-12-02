from typing import Any, Dict, Optional, Union
import httpx


class HttpClientError(Exception):
    """Custom exception for HTTP client errors."""
    def __init__(self, message: str, status_code: int = None, details: Any = None):
        super().__init__(message)
        self.status_code = status_code
        self.details = details


class HttpClient:
    def __init__(self, base_url: str):
        self.client = httpx.AsyncClient(base_url=base_url)

    async def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Any:
        """Send a GET request."""
        try:
            response = await self.client.get(endpoint, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HttpClientError(
                message=f"HTTP error occurred while GET {endpoint}",
                status_code=e.response.status_code,
                details=e.response.text
            )
        except httpx.RequestError as e:
            raise HttpClientError(
                message=f"Request error occurred while GET {endpoint}",
                details=str(e)
            )

    async def post(self, endpoint: str, json: Optional[Dict[str, Any]] = None, data: Optional[Union[Dict[str, Any], Any]] = None, headers: Optional[Dict[str, str]] = None) -> Any:
        """Send a POST request."""
        try:
            response = await self.client.post(endpoint, json=json, data=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HttpClientError(
                message=f"HTTP error occurred while POST {endpoint}",
                status_code=e.response.status_code,
                details=e.response.text
            )
        except httpx.RequestError as e:
            raise HttpClientError(
                message=f"Request error occurred while POST {endpoint}",
                details=str(e)
            )

    async def put(self, endpoint: str, json: Optional[Dict[str, Any]] = None, data: Optional[Union[Dict[str, Any], Any]] = None, headers: Optional[Dict[str, str]] = None) -> Any:
        """Send a PUT request."""
        try:
            response = await self.client.put(endpoint, json=json, data=data, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HttpClientError(
                message=f"HTTP error occurred while PUT {endpoint}",
                status_code=e.response.status_code,
                details=e.response.text
            )
        except httpx.RequestError as e:
            raise HttpClientError(
                message=f"Request error occurred while PUT {endpoint}",
                details=str(e)
            )

    async def delete(self, endpoint: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None) -> Any:
        """Send a DELETE request."""
        try:
            response = await self.client.delete(endpoint, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise HttpClientError(
                message=f"HTTP error occurred while DELETE {endpoint}",
                status_code=e.response.status_code,
                details=e.response.text
            )
        except httpx.RequestError as e:
            raise HttpClientError(
                message=f"Request error occurred while DELETE {endpoint}",
                details=str(e)
            )
