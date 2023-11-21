import requests
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def _send_request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}{endpoint}"
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response.json()
        except HTTPError as http_err:
            print(f"HTTP error occurred: {http_err}")
        except ConnectionError as conn_err:
            print(f"Connection error occurred: {conn_err}")
        except Timeout as timeout_err:
            print(f"Timeout error occurred: {timeout_err}")
        except RequestException as req_err:
            print(f"Request error occurred: {req_err}")
        except Exception as e:
            print(f"An error occurred: {e}")
        return None

    def get_admins(self):
        return self._send_request('GET', '/admins/')

    def create_admin(self, admin_data):
        return self._send_request('POST', '/admins/', json=admin_data)

    def get_clients(self):
        return self._send_request('GET', '/clients/')

    def create_client(self, client_data):
        return self._send_request('POST', '/clients/', json=client_data)

    def get_commands(self):
        return self._send_request('GET', '/commands/')

    def create_command(self, command_data):
        return self._send_request('POST', '/commands/', json=command_data)

    def get_commands_by_client_id(self, client_id):
        return self._send_request('GET', f'/clients/{client_id}/commands/')


