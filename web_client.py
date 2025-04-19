"""
The main client facade for interacting with the api-web.nhle.com API endpoints.
"""
import typing as t
from .http_client import HttpClient
from .config import WEB_BASE_URL
from .web import (
    Players,
    Teams,
    Schedule,
    Game,
    Playoff,
    Draft,
    Misc,
    OtherWeb,
)

class NHLWebClient:
    """
    Asynchronous client for accessing NHL Web API (api-web.nhle.com) endpoints.

    Provides access to various categories of endpoints through attributes like
    `players`, `teams`, `schedule`, etc.

    Usage:
        >>> client = NHLWebClient()
        >>> async with client: # Use as an async context manager
        ...    info = await client.players.get_landing(8477934)
        or
        >>> client = NHLWebClient()
        >>> info = await client.players.get_landing(8477934)
        >>> await client.aclose() # Manually close if not using 'async with'
    """
    def __init__(self, **httpx_kwargs: t.Any):
        """
        Initializes the NHL Web API client.

        Args:
            **httpx_kwargs: Optional keyword arguments passed directly to the
                            underlying httpx.AsyncClient (e.g., timeout, headers, proxies).
        """
        self.http_client = HttpClient(base_url=WEB_BASE_URL, **httpx_kwargs)

        # Initialize endpoint categories, passing the HTTP client
        self.players = Players(self.http_client)
        self.teams = Teams(self.http_client)
        self.schedule = Schedule(self.http_client)
        self.game = Game(self.http_client)
        self.playoff = Playoff(self.http_client)
        self.draft = Draft(self.http_client)
        self.misc = Misc(self.http_client)
        self.other_web = OtherWeb(self.http_client)
        # Add other categories here as they are implemented...

    async def aclose(self) -> None:
        """Closes the underlying HTTP client sessions."""
        await self.http_client.aclose()

    async def __aenter__(self) -> 'NHLWebClient':
        """Enter the async context manager."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the async context manager and close the client."""
        await self.aclose()