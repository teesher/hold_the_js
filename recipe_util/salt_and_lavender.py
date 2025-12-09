from .base import RecipeBase
import logging
from bs4 import BeautifulSoup as bs

LOGGER = logging.getLogger(__name__)

class RecipeSaltAndLavender(RecipeBase):
    def _get_recipe_print_url(self, url: str, soup: bs):
        a_ele = soup.find("a", class_="wprm-recipe-print")
        try:
            return a_ele.get('href')
        except Exception as e:
            LOGGER.warning(f'Print element not found for {url}.')
            return url
