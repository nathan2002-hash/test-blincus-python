import requests

class BlincusRefund:
    def __init__(self, access_key, secret, base_url='http://127.0.0.1:89'):
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
            # Check if token exists in response and print appropriate messages
            if 'token' in response:
                self.token = response['token']
                print(f"Authentication successful! Token: {self.token}")
            else:
                print(f"Authentication failed: {response.get('error', 'Unknown error')}")
        else:
            print("Authentication failed due to an error.")

    def send_payment(self, amount, payment_id, reason, reason_description):
        """
        Send Payment Refund using the Blincus API.
        """
        if not self.token:
            print("Client not authenticated. Call `authenticate()` first.")
            return

        url = f'{self.base_url}/api/sandbox/v1/payment/refund'
        payload = {
            'amount': amount,
            'payment_id': payment_id,
            'reason': reason,
            'reason_description': reason_description,
        }
        headers = {
            'Authorization': f'Bearer {self.token}',
            'Content-Type': 'application/json'
        }

        response = self._make_request(url, payload, headers)
        if response:
            print("Payment Refund successful:", response)
        else:
            print("Payment Refund failed.")

    def _make_request(self, url, payload, headers=None):
        """
        Helper function to handle the HTTP request and error handling.
        """
        try:
            # Send the request
            if headers:
                response = requests.post(url, json=payload, headers=headers)
            else:
                response = requests.post(url, json=payload)

            response.raise_for_status()  # Will raise HTTPError for non-2xx responses
            
            # Return the response in JSON format
            return response.json()

        except requests.exceptions.HTTPError as e:
            # If error occurs, print the server's response error message
            try:
                error_message = response.json().get('error', 'Unknown error')
                print(f"Error: {error_message}")
            except ValueError:
                print(f"HTTP Error occurred: {e}")
            return None

        except requests.RequestException as e:
            print(f"Request error: {str(e)}")
            return None
