from .base import RecipeBase
from bs4 import BeautifulSoup as bs
import logging

LOGGER = logging.getLogger(__name__)

class RecipeFeelGoodFoodie(RecipeBase):
    def _get_recipe_print_url(self, url: str, soup: bs):
        return self._get_wprm_print_url()