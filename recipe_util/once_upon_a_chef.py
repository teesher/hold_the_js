from .base import RecipeBase
from bs4 import BeautifulSoup as bs
import logging


LOGGER = logging.getLogger(__name__)

class RecipeOnceUponAChef(RecipeBase):
    def _get_recipe_print_url(self, url: str, soup: bs):
        return f"{url}?recipe_print=yes"
