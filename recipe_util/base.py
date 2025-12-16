import abc
import re
import logging
import requests
from bs4 import BeautifulSoup as bs
from util.constants import REQUEST_HEADERS

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
        try:
            response = requests.get(
                url=self.url, 
                headers=REQUEST_HEADERS, 
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
    
    @abc.abstractmethod
    def _get_recipe_print_url(self):
        raise NotImplementedError()

