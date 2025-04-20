"""
The main client facade for interacting with the api.nhle.com/stats/rest API endpoints.
"""
import typing as t
from .http_client import HttpClient
from .config import STATS_BASE_URL
from .stats import (
    StatsPlayers,
    StatsTeams,
    StatsDraft,
    StatsSeason,
    StatsGame,
    StatsMisc,
)

DEFAULT_LANGUAGE = "en"

class NHLStatsClient:
    """
    Asynchronous client for accessing NHL Stats API (api.nhle.com/stats/rest) endpoints.

    Provides access to various categories of endpoints through attributes like
    `players`, `teams`, `game`, etc.

    Most Stats API endpoints require a language code prefix (e.g., '/en/').
    This client handles adding the language code automatically based on the
    `language` parameter provided during initialization (defaults to 'en').

    Usage:
        >>> # Default language ('en')
        >>> client = NHLStatsClient()
        >>> async with client:
        ...    info = await client.players.get_skater_leaders("points")

        >>> # Specify language
        >>> client_fr = NHLStatsClient(language='fr')
        >>> async with client_fr:
        ...    info_fr = await client_fr.teams.get_info()

        >>> # Manual closing
        >>> client = NHLStatsClient()
        >>> info = await client.misc.ping() # Ping doesn't use language
        >>> await client.aclose()
    """
    def __init__(self, language: str = DEFAULT_LANGUAGE, **httpx_kwargs: t.Any):
        """
        Initializes the NHL Stats API client.

        Args:
            language: The language code to use for API requests (e.g., 'en', 'fr').
                      Defaults to 'en'.
            **httpx_kwargs: Optional keyword arguments passed directly to the
                            underlying httpx.AsyncClient (e.g., timeout, headers, proxies).
        """
        # Base URL *without* language, as it's prepended in requests by the category base class
        self.http_client = HttpClient(base_url=STATS_BASE_URL, **httpx_kwargs)
        self.language = language.lower() # Store language for endpoint categories

        # Initialize endpoint categories, passing the HTTP client and language
        self.players = StatsPlayers(self.http_client, self.language)
        self.teams = StatsTeams(self.http_client, self.language)
        self.draft = StatsDraft(self.http_client, self.language)
        self.season = StatsSeason(self.http_client, self.language)
        self.game = StatsGame(self.http_client, self.language)
        self.misc = StatsMisc(self.http_client, self.language)
        # Add other categories here if the API expands further

    async def aclose(self) -> None:
        """Closes the underlying HTTP client sessions."""
        await self.http_client.aclose()

    async def __aenter__(self) -> 'NHLStatsClient':
        """Enter the async context manager."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the async context manager and close the client."""
        await self.aclose()