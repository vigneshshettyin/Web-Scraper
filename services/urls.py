'''
Url Validation and Cleaning Class
'''
import re


class UrlValidators:
    '''
    This class validates the url
    '''

    def clean_url(self, url):
        '''
        This function cleans the url
        '''
        url = url.strip()
        if url.startswith('http://'):
            url = url[7:]
        elif url.startswith('https://'):
            url = url[8:]
        url = 'https://' + url
        return url

    def validate_url(self, url):
        '''
        This function validates the url
        '''
        rgx = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            # domain...
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
            r'localhost|'  # localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return re.match(rgx, url)
