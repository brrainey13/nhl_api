import pytest

@pytest.fixture
def mock_player_landing_success():
    return {
        "playerId": 8477934,
        "firstName": {"default": "Auston"},
        "lastName": {"default": "Matthews"},
        # Add more fields as needed for your test
    }

@pytest.fixture
def mock_not_found():
    # This can be used to trigger not found logic, or left empty if not needed
    pass
