from .recipe_search_base import (
    RecipeSearchBase
)
import logging


LOGGER = logging.getLogger(__name__)

class RecipeSearchOnceUponAChef(RecipeSearchBase):
    def _get_recipe_print_url(self, url, _):
        return f"{url}?recipe_print=yes"
