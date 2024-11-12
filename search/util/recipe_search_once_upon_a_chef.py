from .recipe_search_base import (
    RecipeSearchBase, 
    STATUS_CODE_OK, 
    DEFAULT_TIMEOUT
)
from urllib.parse import quote
from bs4 import BeautifulSoup as bs
import requests
import logging


LOGGER = logging.getLogger(__name__)

class RecipeSearchOnceUponAChef(RecipeSearchBase):
    def _get_recipe_result_urls(self, search_string: str):
        recipe_result_urls = []
        url_safe_search_string = quote(search_string)
        url = self._base_url + self._base_url_search_path + url_safe_search_string

        response = requests.get(url=url, timeout=DEFAULT_TIMEOUT)

        if response.status_code == STATUS_CODE_OK:
            soup = bs(response.text, "html.parser")

            # find list of search results
            ul_ele = soup.find("ul", {"class": "ajaxresults"}) # config?

            # find urls to recipes
            for a_ele in ul_ele.find_all("a"):
                recipe_result_urls.append(a_ele.get('href'))
        else:
            # TODO set up django error handling
            LOGGER.error("Bad request")

        return recipe_result_urls
    
    def _get_recipe_print_urls(self, recipe_result_urls: list):
        recipe_print_urls = []

        for recipe_result_url in recipe_result_urls:
            recipe_print_urls.append(f"{recipe_result_url}?recipe_print=yes")

        return recipe_print_urls
