"""
NHL API Wrapper Library
~~~~~~~~~~~~~~~~~~~~~~~

An asynchronous Python wrapper for the official NHL APIs.

Usage:

   >>> import asyncio
   >>> from nhl_api import NHLWebClient
   >>>
   >>> async def main():
   ...     async with NHLWebClient() as client:
   ...         player_info = await client.players.get_landing(player_id=8477934)
   ...         print(player_info['firstName']['default'])
   >>>
   >>> asyncio.run(main())

"""

__version__ = "0.1.0"

from .exceptions import NHLAPIError, NHLRateLimitError, NHLServerError, NHLNotFoundError, NHLBadRequestError
from .web_client import NHLWebClient
# from .stats_client import NHLStatsClient # Uncomment when Phase 2 is done

__all__ = [
    "NHLAPIError",
    "NHLRateLimitError",
    "NHLServerError",
    "NHLNotFoundError",
    "NHLBadRequestError",
    "NHLWebClient",
    # "NHLStatsClient", # Uncomment when Phase 2 is done
]