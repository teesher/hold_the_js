from .recipe_base import (
    RecipeBase
)
import logging


LOGGER = logging.getLogger(__name__)

class RecipeOnceUponAChef(RecipeBase):
    def _get_recipe_print_url(self, url, soup):
        return f"{url}?recipe_print=yes"
