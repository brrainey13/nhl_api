# NHL API Python Wrapper

An asynchronous Python wrapper for the official (but undocumented) NHL APIs:
`api-web.nhle.com` and `api.nhle.com/stats/rest`.

**Note:** This library interacts with APIs that are not officially documented or supported by the NHL. Use at your own risk. API changes may break this library without notice.

## Installation

```bash
pip install git+https://github.com/brrainey13/nhl-api.git # Or clone and pip install .
```

Or for development:
```bash
git clone https://github.com/brrainey13/nhl-api.git
cd nhl-api
pip install -e .
```

## Basic Usage (api-web.nhle.com)

```python
import asyncio
from nhl_api import NHLWebClient
from nhl_api.exceptions import NHLAPIError

async def main():
    # You can pass httpx.AsyncClient options here, e.g., timeout=15
    async with NHLWebClient() as client:
        try:
            # Get player landing info (Auston Matthews)
            player_info = await client.players.get_landing(player_id=8477934)
            print(f"Player: {player_info['firstName']['default']} {player_info['lastName']['default']}")
            print(f"Team: {player_info['currentTeamAbbrev']}")
            print(f"Position: {player_info['position']}")

            # Get today's standings
            standings = await client.teams.get_standings_now()
            print(f"\nStandings Date: {standings['standingsDate']}")
            # Loop through standings['standings'] for details

            # Get game log for Connor McDavid, 2023-2024 Regular Season
            game_log = await client.players.get_game_log(
                player_id=8478402,
                season=20232024,
                game_type=2 # 2=Regular Season, 3=Playoffs
            )
            print(f"\nMcDavid Game Log (First 5 Games):")
            for game in game_log['gameLog'][:5]:
                 print(f"  Date: {game['gameDate']}, Opp: {game['opponentAbbrev']}, G: {game['goals']}, A: {game['assists']}")

            # Get schedule for a specific date
            schedule = await client.schedule.get_schedule_by_date(date="2023-11-10")
            print(f"\nSchedule for 2023-11-10:")
            for date_info in schedule['gameWeek']:
                if date_info['date'] == "2023-11-10":
                    for game in date_info['games']:
                        print(f"  {game['awayTeam']['abbrev']} @ {game['homeTeam']['abbrev']} ({game['gameTypeDescription']}) - State: {game['gameState']}")


        except NHLAPIError as e:
            print(f"API Error: Status={e.status_code}, Message={e.message}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())