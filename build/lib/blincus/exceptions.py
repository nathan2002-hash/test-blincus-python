class BlincusAuthenticationError(Exception):
    """Raised when authentication with the Blincus API fails."""
    pass

class BlincusRequestError(Exception):
    """Raised when a request to the Blincus API fails."""
    pass
