'''
This is a network service which gets the network information
'''
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests


class NetworkService:
    '''
    Network service uses ip-api.com to get the network information
    '''

    SERVICE_URL = 'http://ip-api.com/json/'

    WHOIS_URL = 'https://www.whois.com/whois/'

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

    def get_whois_data(self, url):
        '''
        This function returns the whois data
        '''
        domain_name = self.get_domain_name(url)
        request_url = self.WHOIS_URL + domain_name
        try:
            response = requests.get(request_url, timeout=5)
            if response.status_code == 200:
                bs4_soup = BeautifulSoup(response.text, 'lxml')
                whois_data = bs4_soup.find('pre').text
                whois_data = whois_data.splitlines()
                whois_data = [x.split(':') for x in whois_data]
                whois_data = [x for x in whois_data if len(
                    x) == 2 and x[0] != '']
                whois_data = {x[0].strip(): x[1].strip() for x in whois_data}
                return whois_data
            else:
                return self.get_request_error_msg()
        except requests.exceptions.RequestException:
            return self.get_request_error_msg()

    def get_data(self, url):
        '''
        This function returns the network information
        '''
        data = {}
        data['whois_info'] = self.get_whois_data(url)
        data['network_info'] = self.get_network_info(url)
        if data:
            return data
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
