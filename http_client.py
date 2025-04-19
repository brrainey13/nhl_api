"""
Core asynchronous HTTP client for interacting with NHL APIs.
"""
import httpx
import typing as t
from .config import DEFAULT_TIMEOUT
from .exceptions import (
    NHLAPIError,
    NHLBadRequestError,
    NHLNotFoundError,
    NHLRateLimitError,
    NHLServerError
)

class HttpClient:
    """A wrapper around httpx.AsyncClient for making API calls."""

    def __init__(self, base_url: str, timeout: float = DEFAULT_TIMEOUT, **httpx_kwargs):
        """
        Initializes the HTTP client.

        Args:
            base_url: The base URL for the API.
            timeout: Default request timeout in seconds.
            **httpx_kwargs: Additional arguments to pass to httpx.AsyncClient (e.g., headers).
        """
        self.base_url = base_url.rstrip("/")
        self._client = httpx.AsyncClient(base_url=self.base_url, timeout=timeout, follow_redirects=True, **httpx_kwargs)
        # Consider adding a default User-Agent header here if desired
        # self._client.headers['User-Agent'] = USER_AGENT

    async def get(self, path: str, params: t.Optional[t.Dict[str, t.Any]] = None) -> t.Dict[str, t.Any]:
        """
        Performs an asynchronous GET request.

        Args:
            path: The API endpoint path (relative to base_url).
            params: Optional dictionary of query parameters.

        Returns:
            The JSON response parsed as a dictionary.

        Raises:
            NHLAPIError: If the API returns an error status code (>= 400).
            httpx.RequestError: For network-related issues.
        """
        url_path = path.lstrip("/")
        request_url = self._client.build_request("GET", url_path, params=params).url
        try:
            response = await self._client.get(url_path, params=params)

            # Check for specific error codes first
            if response.status_code == 400:
                raise NHLBadRequestError(response.status_code, response.text, str(request_url))
            if response.status_code == 404:
                raise NHLNotFoundError(response.status_code, response.text, str(request_url))
            if response.status_code == 429:
                raise NHLRateLimitError(response.status_code, response.text, str(request_url))
            if response.status_code >= 500:
                raise NHLServerError(response.status_code, response.text, str(request_url))

            # General check for other 4xx errors
            response.raise_for_status() # Raises httpx.HTTPStatusError for 4xx Client Errors

            # Attempt to parse JSON, handle potential errors
            try:
                return response.json()
            except ValueError: # Includes JSONDecodeError
                 raise NHLAPIError(response.status_code, "Failed to decode JSON response", str(request_url))

        except httpx.HTTPStatusError as e:
            # Catch errors raised by raise_for_status() for other 4xx codes
             raise NHLAPIError(e.response.status_code, e.response.text, str(e.request.url)) from e
        # Allow httpx.RequestError (network issues, timeouts) to propagate naturally
        # Or catch and wrap them if you prefer:
        # except httpx.RequestError as e:
        #     raise NHLAPIError(0, f"Network error: {e}", str(e.request.url)) from e


    async def aclose(self):
        """Closes the underlying httpx client."""
        await self._client.aclose()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.aclose()