import pytest
import pytest_asyncio
import httpx
from pytest_httpx import HTTPXMock

# If you install pytest-httpx: pip install pytest-httpx

@pytest.fixture
def mock_httpx(httpx_mock: HTTPXMock):
    """Provides a mocked HTTpx interface."""
    return httpx_mock

# Example: Define standard mock responses
@pytest.fixture
def mock_player_landing_success(mock_httpx: HTTPXMock):
    player_id = 8477934 # Matthews
    url = f"https://api-web.nhle.com/v1/player/{player_id}/landing"
    mock_data = {
        "playerId": player_id,
        "firstName": {"default": "Auston"},
        "lastName": {"default": "Matthews"},
        "currentTeamAbbrev": "TOR",
        "position": "C",
        # Add more fields as needed for tests
    }
    mock_httpx.add_response(url=url, method="GET", json=mock_data, status_code=200)
    return mock_data # Return the data for assertion comparison

@pytest.fixture
def mock_not_found(mock_httpx: HTTPXMock):
    url_pattern = "https://api-web.nhle.com/v1/*"
    mock_httpx.add_response(
        url__regex=url_pattern, # Match any path under /v1/ for simplicity
        method="GET",
        status_code=404,
        text="Not Found"
    )