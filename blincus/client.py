import requests

class BlincusClient:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.auth_url = 'http://localhost:89/api/token'
        self.transaction_url = 'http://localhost:89/api/sandbox/v1/payment'
        self.access_token = None

    def get_access_token(self):
        data = {
            'email': self.email,
            'password': self.password,
        }

        try:
            response = requests.post(self.auth_url, json=data)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

            json_data = response.json()
            self.access_token = json_data.get('access_token', {}).get('token')
            return self.access_token
        except requests.exceptions.RequestException as e:
            print("Error getting access token:", e)
            return None

    def make_transaction(self, transaction_data):
        if not self.access_token:
            raise ValueError("Access token not set. Call get_access_token() first.")

        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        try:
            response = requests.post(self.transaction_url, headers=headers, json=transaction_data)
            response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

            return response.json()
        except requests.exceptions.RequestException as e:
            print("Error making transaction:", e)
            return None
