import pytest
import asyncio
import json
from nhl_api.web.teams import Teams
from nhl_api.web.schedule import Schedule
from nhl_api.web.game import Game
from nhl_api.web.playoff import Playoff
from nhl_api.web.other_web import OtherWeb
from nhl_api.web.misc import Misc
from nhl_api.web.players import Players
from nhl_api.web.draft import Draft
from nhl_api.http_client import HttpClient
from nhl_api.config import WEB_BASE_URL

def get_test_args(method_name):
    """Return a dict of test arguments for each method name."""
    return {
        # Teams
        "get_standings_by_date": {"date": "2024-04-15"},
        "get_club_stats_now": {"team_tricode": "TOR"},
        "get_club_stats_season_summary": {"team_tricode": "TOR"},
        "get_club_stats_by_season": {"team_tricode": "TOR", "season": 20232024, "game_type": 2},
        "get_team_scoreboard_now": {"team_tricode": "TOR"},
        "get_roster_now": {"team_tricode": "TOR"},
        "get_roster_by_season": {"team_tricode": "TOR", "season": 20232024},
        "get_roster_season_summary": {"team_tricode": "TOR"},
        "get_prospects": {"team_tricode": "TOR"},
        # Schedule
        "get_team_season_schedule_now": {"team_tricode": "TOR"},
        "get_team_season_schedule": {"team_tricode": "TOR", "season": 20232024},
        "get_team_month_schedule_now": {"team_tricode": "TOR"},
        "get_team_month_schedule": {"team_tricode": "TOR", "month": "2024-04"},
        "get_team_week_schedule": {"team_tricode": "TOR", "date": "2024-04-15"},
        "get_team_week_schedule_now": {"team_tricode": "TOR"},
        "get_schedule_by_date": {"date": "2024-04-15"},
        "get_schedule_calendar_by_date": {"date": "2024-04-15"},
        # Game
        "get_scores_by_date": {"date": "2024-04-15"},
        "get_play_by_play": {"game_id": 2023020001},
        "get_landing": {"game_id": 2023020001},
        "get_boxscore": {"game_id": 2023020001},
        "get_game_story": {"game_id": 2023020001},
        "get_goal_replay": {"game_id": 2023020001, "event_id": 1},
        "get_play_replay": {"game_id": 2023020001, "event_id": 1},
        "get_game_right_rail": {"game_id": 2023020001},
        "get_wsc_play_by_play": {"game_id": 2023020001},
        # Playoff
        "get_series_carousel": {"season": 20232024},
        "get_series_schedule": {"season": 20232024, "series_letter": "A"},
        "get_bracket": {"year": 2024},
        "get_series_metadata": {"year": 2024, "series_letter": "A"},
        # OtherWeb
        "get_where_to_watch": {},
        "get_tv_schedule_by_date": {"date": "2024-04-15"},
        "get_partner_game_odds_now": {"country_code": "US"},
        # Misc
        "get_meta_info": {},
        "get_meta_game_info": {"game_id": 2023020001},
        "get_postal_code_info": {"postal_code": "10001"},
        # Players
        "get_game_log": {"player_id": 8478402, "season": 20232024, "game_type": 2},
        "get_landing": {"player_id": 8478402},
        "get_game_log_now": {"player_id": 8478402},
        "get_skater_stats_leaders_current": {"categories": None, "limit": 5},
        "get_skater_stats_leaders_by_season": {"season": 20232024, "game_type": 2, "categories": None, "limit": 5},
        "get_goalie_stats_leaders_current": {"categories": None, "limit": 5},
        "get_goalie_stats_leaders_by_season": {"season": 20232024, "game_type": 2, "categories": None, "limit": 5},
        "get_player_spotlight": {},
        # Draft
        "get_rankings_now": {},
        "get_rankings_by_prospect_category": {"season_year": 2023, "prospect_category": 1},
        "get_tracker_picks_now": {},
        "get_picks_now": {},
        "get_picks_by_season": {"season_year": 2023, "round_number": "all"},
    }.get(method_name, {})

WRAPPER_METHODS = [
    (Teams, [
        "get_standings_now",
        "get_standings_by_date",
        "get_standings_season_info",
        "get_club_stats_now",
        "get_club_stats_season_summary",
        "get_club_stats_by_season",
        "get_team_scoreboard_now",
        "get_roster_now",
        "get_roster_by_season",
        "get_roster_season_summary",
        "get_prospects",
    ]),
    (Schedule, [
        "get_team_season_schedule_now",
        "get_team_season_schedule",
        "get_team_month_schedule_now",
        "get_team_month_schedule",
        "get_team_week_schedule",
        "get_team_week_schedule_now",
        "get_schedule_now",
        "get_schedule_by_date",
        "get_schedule_calendar_now",
        "get_schedule_calendar_by_date",
    ]),
    (Game, [
        "get_scores_now",
        "get_scores_by_date",
        "get_scoreboard_now",
        "get_play_by_play",
        "get_landing",
        "get_boxscore",
        "get_game_story",
        "get_goal_replay",
        "get_play_replay",
        "get_game_right_rail",
        "get_wsc_play_by_play",
    ]),
    (Playoff, [
        "get_series_carousel",
        "get_series_schedule",
        "get_bracket",
        "get_series_metadata",
    ]),
    (OtherWeb, [
        "get_where_to_watch",
        "get_tv_schedule_by_date",
        "get_tv_schedule_now",
        "get_partner_game_odds_now",
        "get_seasons",
    ]),
    (Misc, [
        "get_meta_info",
        "get_meta_game_info",
        "get_location",
        "get_postal_code_info",
        "get_openapi_spec",
    ]),
    (Players, [
        "get_game_log",
        "get_landing",
        "get_game_log_now",
        "get_skater_stats_leaders_current",
        "get_skater_stats_leaders_by_season",
        "get_goalie_stats_leaders_current",
        "get_goalie_stats_leaders_by_season",
        "get_player_spotlight",
    ]),
    (Draft, [
        "get_rankings_now",
        "get_rankings_by_prospect_category",
        "get_tracker_picks_now",
        "get_picks_now",
        "get_picks_by_season",
    ]),
]

@pytest.mark.asyncio
async def test_all_web_routes():
    """Test every public method in every NHL API web wrapper class and print the JSON response."""
    client = HttpClient(WEB_BASE_URL)
    with open("test_output.txt", "w", encoding="utf-8") as f:
        for wrapper_class, method_names in WRAPPER_METHODS:
            instance = wrapper_class(client)
            for method_name in method_names:
                method = getattr(instance, method_name, None)
                if method is None:
                    f.write(f"Method {method_name} not found in {wrapper_class.__name__}\n")
                    continue
                kwargs = get_test_args(method_name)
                f.write(f"\nCalling {wrapper_class.__name__}.{method_name}({kwargs})\n")
                try:
                    result = await method(**kwargs)
                    f.write(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
                except Exception as e:
                    f.write(f"ERROR calling {wrapper_class.__name__}.{method_name}: {e}\n")
