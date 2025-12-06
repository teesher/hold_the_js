import abc
import logging
import requests
from bs4 import BeautifulSoup as bs

STATUS_CODE_OK = 200
DEFAULT_TIMEOUT = 300

class RecipeSearchBase():
    def __init__(self, url):
        self.url = url

    def get_recipe_print_url(self):
        print(f"getting recipe print URL for {self.url}")
        return self._get_recipe_print_url(self.url, self._retrieve_soup_from_url())
    
    def _retrieve_soup_from_url(self):
        print("Retrieving soup. . .")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        response = requests.get(url=self.url, headers=headers, timeout=DEFAULT_TIMEOUT)
        if response.status_code == STATUS_CODE_OK:
            return bs(response.text, "html.parser")
        else:
            print(f"Bad request - Status code: {response.status_code}")
    
    @abc.abstractmethod
    def _get_recipe_print_url(self):
        raise NotImplementedError()

