import requests
from .exceptions import BlincusAuthenticationError, BlincusRequestError

class BlincusClient:
    def __init__(self, access_key, secret, base_url='https://api.blincus.com'):
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
            response.raise_for_status()

            self.token = response.json().get('token')
            if not self.token:
                raise BlincusAuthenticationError("Failed to retrieve token")
        except requests.RequestException as e:
            raise BlincusAuthenticationError(f"Authentication failed: {e}")

    def send_message(self, sender_id, type_, phone_number, message):
        """
        Send an SMS message using the Blincus API.
        """
        if not self.token:
            raise BlincusAuthenticationError("Client not authenticated. Call `authenticate()` first.")

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
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise BlincusRequestError(f"Message sending failed: {e}")
