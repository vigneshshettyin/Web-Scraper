'''
This is a network service which gets the network information
'''
from urllib.parse import urlparse

import requests


class NetworkService:
    '''
    Network service uses ip-api.com to get the network information
    '''

    SERVICE_URL = 'http://ip-api.com/json/'

    def get_domain_name(self, url):
        '''
        This function returns the domain name of the url
        '''
        return urlparse(url).netloc

    def get_network_info(self, url):
        '''
        This makes a request to the ip-api.com and returns the network information
        '''
        request_url = self.SERVICE_URL + self.get_domain_name(url)
        try:
            response = requests.get(request_url, timeout=5)
            if response.status_code == 200:
                return response.json()
            else:
                return self.get_request_error_msg()
        except requests.exceptions.RequestException:
            return self.get_request_error_msg()

    def get_data(self, url):
        '''
        This function returns the network information
        '''
        network_info = self.get_network_info(url)
        if network_info:
            return network_info
        else:
            return self.get_request_error_msg()

    def get_request_error_msg(self):
        '''
        This function returns the error message
        '''
        return {
            'status': 'error',
            'message': 'Error in getting network information'
        }


# user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
# user_ip = "24.48.0.1"
# user_agent_json = json.loads(json.dumps(request.headers.get('User-Agent')))
