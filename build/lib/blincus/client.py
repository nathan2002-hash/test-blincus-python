import requests

class BlincusAuthenticationError(Exception):
    """Raised when authentication fails."""
    def __init__(self, message="Authentication failed", status_code=None):
        super().__init__(message)
        self.status_code = status_code

class BlincusRequestError(Exception):
    """Raised when an API request fails."""
    def __init__(self, message="API request failed", status_code=None, response_body=None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body

class BlincusClient:
    AuthenticationError = BlincusAuthenticationError
    RequestError = BlincusRequestError

    def __init__(self, access_key, secret, base_url='http://192.168.254.25:89'):
        """
        Initialize the Blincus client with authentication details.
        """
        self.access_key = access_key
        self.secret = secret
        self.base_url = base_url
        self.token = None

    def authenticate(self):
        """
        Authenticate with the Blincus API to get a token.
        """
        url = f'{self.base_url}/api/v1/authenticate'
        payload = {'access_key': self.access_key, 'secret': self.secret}

        try:
            response = requests.post(url, json=payload)
            if response.status_code != 200:
                raise self.AuthenticationError(
                    message=f"Authentication failed: {response.text}",
                    status_code=response.status_code
                )
            self.token = response.json().get('token')
            if not self.token:
                raise self.AuthenticationError("Token missing in the response")
        except requests.RequestException as e:
            raise self.AuthenticationError(f"Authentication failed: {str(e)}")

    def send_message(self, sender_id, type_, phone_number, message):
        """
        Send an SMS message using the Blincus API.
        """
        if not self.token:
            raise self.AuthenticationError("Client not authenticated. Call `authenticate()` first.")

        url = f'{self.base_url}/api/sandbox/v1/sms'
        payload = {
            'sender_id': sender_id,
            'type': type_,
            'phone_number': phone_number,
            'message': message
        }
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            if response.status_code != 201:
                raise self.RequestError(
                    message=f"Message failed: {response.text}",
                    status_code=response.status_code,
                    response_body=response.json() if response.content else None
                )
            return response.json()
        except requests.RequestException as e:
            raise self.RequestError(f"Message sending failed: {str(e)}")
