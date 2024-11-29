import requests

class BlincusClient:
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

        response = self._make_request(url, payload)
        if response:
            self.token = response.get('token')
            if not self.token:
                print("Authentication failed: Token missing in the response")
                return
            print("Authentication successful!")
        else:
            print("Authentication failed")

    def send_message(self, sender_id, type_, phone_number, message):
        """
        Send an SMS message using the Blincus API.
        """
        if not self.token:
            print("Client not authenticated. Call `authenticate()` first.")
            return

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

        response = self._make_request(url, payload, headers)
        if response:
            print("Message sent successfully:", response)
        else:
            print("Message sending failed")

    def _make_request(self, url, payload, headers=None):
        """
        Helper function to handle the HTTP request and error handling.
        """
        try:
            if headers:
                response = requests.post(url, json=payload, headers=headers)
            else:
                response = requests.post(url, json=payload)

            response.raise_for_status()  # Will raise HTTPError for non-2xx responses
            return response.json()
        
        except requests.exceptions.HTTPError as e:
            # Output the error message from the server
            error_message = response.json().get('error', 'Unknown error')
            print(f"Error: {error_message}")
            return None

        except requests.RequestException as e:
            print(f"Request error: {str(e)}")
            return None
