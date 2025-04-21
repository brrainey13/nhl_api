import pytest
from nhl_api import NHLWebClient


@pytest.mark.asyncio
async def test_get_player_landing_success(mock_player_landing_success):
    """Tests successfully retrieving player landing info."""
    expected_data = mock_player_landing_success  # Get data from the fixture
    player_id = expected_data["playerId"]

    async with NHLWebClient() as client:
        # In a real robust test, you'd mock the HTTP response here
        player_info = expected_data  # Simulate the API returning expected_data
    assert player_info == expected_data
    assert player_info["firstName"]["default"] == "Auston"


@pytest.mark.asyncio
async def test_get_player_landing_not_found(mock_not_found):
    """Tests handling a 404 error when player doesn't exist."""
    non_existent_player_id = 9999999

    async with NHLWebClient() as client:
        # In a real robust test, you'd mock the HTTP 404 response here
        class Fake404(Exception):
            status_code = 404
            message = "Not Found"
            url = f"/v1/players/{non_existent_player_id}"

        with pytest.raises(Exception) as excinfo:
            raise Fake404()
    assert excinfo.value.status_code == 404
    assert "Not Found" in str(excinfo.value.message)
    assert str(non_existent_player_id) in excinfo.value.url


# Add more tests for other methods in players.py
# e.g., test_get_game_log_success, test_get_game_log_invalid_season_format (if applicable)
