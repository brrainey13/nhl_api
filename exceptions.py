"""
Custom exceptions for the NHL API Wrapper.
"""

class NHLAPIError(Exception):
    """Base exception class for NHL API errors."""
    def __init__(self, status_code: int, message: str, url: str):
        self.status_code = status_code
        self.message = message
        self.url = url
        super().__init__(f"HTTP {status_code} for {url}: {message}")

class NHLBadRequestError(NHLAPIError):
    """Exception for 400 Bad Request errors."""
    def __init__(self, status_code: int, message: str, url: str):
        super().__init__(status_code, message, url)


class NHLNotFoundError(NHLAPIError):
    """Exception for 404 Not Found errors."""
    def __init__(self, status_code: int, message: str, url: str):
        super().__init__(status_code, message, url)

class NHLRateLimitError(NHLAPIError):
    """Exception for 429 Too Many Requests errors."""
    def __init__(self, status_code: int, message: str, url: str):
        super().__init__(status_code, message, url)

class NHLServerError(NHLAPIError):
    """Exception for 5xx Server errors."""
    def __init__(self, status_code: int, message: str, url: str):
        super().__init__(status_code, message, url)

# You could add more specific 4xx errors if needed (e.g., 401 Unauthorized, 403 Forbidden)