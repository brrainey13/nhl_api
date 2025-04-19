"""
Configuration constants for the NHL API Wrapper.
"""

# Base URLs for the two main APIs
WEB_BASE_URL = "https://api-web.nhle.com"
STATS_BASE_URL = "https://api.nhle.com/stats/rest" # Note: Language code will be prepended

# Default timeout for HTTP requests in seconds
DEFAULT_TIMEOUT = 10.0

# User Agent String (Optional, but can be polite)
# Some APIs might block default httpx/python user agents eventually
# USER_AGENT = f"nhl-api-wrapper-python/{__version__}" # Requires importing __version__ carefully