from .recipe_search_base import (
    RecipeSearchBase
)
import logging


LOGGER = logging.getLogger(__name__)

class RecipeSearchOnceUponAChef(RecipeSearchBase):
    def _get_recipe_result_urls(self):
        recipe_result_urls = []

        # Find list of search results
        ul_ele = self._search_soup.find("ul", {"class": "ajaxresults"}) # config?

        # Find urls to recipes
        for a_ele in ul_ele.find_all("a"):
            recipe_result_urls.append(a_ele.get('href'))

        return recipe_result_urls
    
    def _get_recipe_print_urls(self, recipe_result_urls: list):
        recipe_print_urls = []

        for recipe_result_url in recipe_result_urls:
            recipe_print_urls.append(f"{recipe_result_url}?recipe_print=yes")

        return recipe_print_urls
    
    def _get_recipe_names(self):
        recipe_names = []
        # Find list of search results
        ul_ele = self._search_soup.find("ul", {"class": "ajaxresults"}) # config?

        # Find names of recipes
        for a_ele in ul_ele.find_all("a"):
            recipe_names.append(a_ele.text)

        return recipe_names
    
    def _get_recipe_image_urls(self):
        recipe_image_urls = []
        # Find list of search results
        ul_ele = self._search_soup.find("ul", {"class": "ajaxresults"}) # config?

        # Find image urls of recipes
        for img_ele in ul_ele.find_all("img"):
            recipe_image_urls.append(img_ele['src'])

        return recipe_image_urls
