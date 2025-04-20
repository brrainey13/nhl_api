"""
NHL API Wrapper Library
~~~~~~~~~~~~~~~~~~~~~~~

An asynchronous Python wrapper for the official NHL APIs.

Usage:

   >>> import asyncio
   >>> from nhl_api import NHLWebClient, NHLStatsClient
   >>>
   >>> async def main():
   ...     async with NHLWebClient() as web_client, NHLStatsClient() as stats_client:
   ...         # Web API call
   ...         player_info = await web_client.players.get_landing(player_id=8477934)
   ...         print(f"Web API: {player_info['firstName']['default']}")
   ...
   ...         # Stats API call
   ...         skater_leaders = await stats_client.players.get_skater_leaders("points")
   ...         print(f"Stats API: Top points leader = {skater_leaders['data'][0]['player']['fullName']}")
   >>>
   >>> asyncio.run(main())

"""

__version__ = "0.1.0" # Consider incrementing version (e.g., 0.2.0)

from .exceptions import NHLAPIError, NHLRateLimitError, NHLServerError, NHLNotFoundError, NHLBadRequestError
from .web_client import NHLWebClient
from .stats_client import NHLStatsClient # Uncommented

__all__ = [
    "NHLAPIError",
    "NHLRateLimitError",
    "NHLServerError",
    "NHLNotFoundError",
    "NHLBadRequestError",
    "NHLWebClient",
    "NHLStatsClient", # Added
]