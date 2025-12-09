import abc
import re
import logging
import requests
from bs4 import BeautifulSoup as bs

STATUS_CODE_OK = 200
# Reduced timeout from 300s to 30s to prevent resource exhaustion
DEFAULT_TIMEOUT = 30

class RecipeBase():
    def __init__(self, url, base_url):
        """
        Initialize with a URL.
        """
        self.url = url
        self.base_url = base_url
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_recipe_print_url(self):
        """
        Get the print-friendly URL for the recipe.
        
        Returns:
            str: The print URL
        """
        self.logger.info(f"Getting recipe print URL for {self.url}")
        return self._get_recipe_print_url(
            url=self.url, 
            soup=self._retrieve_soup_from_url()
        )
    
    def _retrieve_soup_from_url(self) -> bs:
        """
        Retrieve and parse HTML from the URL.
        
        Returns:
            BeautifulSoup object or None
        """
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        try:
            response = requests.get(
                url=self.url, 
                headers=headers, 
                timeout=DEFAULT_TIMEOUT
            )
            
            if response.status_code == STATUS_CODE_OK:
                self.logger.info(f"Request successful for: {self.url}")
                return bs(response.text, "html.parser")
            else:
                self.logger.warning(f"Bad request - Status code: {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            self.logger.error(f"Request timed out after {DEFAULT_TIMEOUT}s")
            return None
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request failed: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}")
            return None
        
    def _get_wprm_print_url(self):
        wprm_print_url = f"{self.base_url}/wprm_print{self.url.replace(self.base_url, '')}"
        soup = self._retrieve_soup_from_url()

        if wprm_print_url in soup.text:
            return wprm_print_url
        else:
            # sometimes print url is not exactly same as on initial recipe page
            print_a_tags = soup.find_all("a", href=re.compile(f"{self.base_url}/wprm_print/"))
            return print_a_tags[0]["href"]
    
    @abc.abstractmethod
    def _get_recipe_print_url(self):
        raise NotImplementedError()

