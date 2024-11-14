from .recipe_search_base import (
    RecipeSearchBase
)
import logging
import re

LOGGER = logging.getLogger(__name__)

class RecipeSearchSaltAndLavender(RecipeSearchBase):
    def _get_recipe_result_urls(self):
        recipe_result_urls = []

        parents = self._search_soup.find_all("h2", {"class": "post-summary__title"})  
        for parent in parents:
            a_ele = parent.find("a")
            recipe_result_urls.append(a_ele.get('href'))

        return recipe_result_urls
    
    def _get_recipe_names(self):
        recipe_names = []

        parents = self._search_soup.find_all("h2", {"class": "post-summary__title"})  
        for parent in parents:
            a_ele = parent.find("a")
            recipe_names.append(a_ele.text)

        return recipe_names
    
    def _get_recipe_image_urls(self):
        recipe_image_urls = []

        parents = self._search_soup.find_all("div", {"class": "post-summary__image"})  
        for parent in parents:
            img_ele = parent.find("img")
            recipe_image_urls.append(img_ele['src'])

        return recipe_image_urls

    def _get_recipe_print_urls(self, recipe_result_urls: list):
        recipe_print_urls = []

        for recipe_result_url in recipe_result_urls:
            recipe_soup = self._retrieve_soup_from_url(recipe_result_url)
            a_ele = recipe_soup.find("a", {"class": "wprm-recipe-print"})
            try:
                recipe_print_urls.append(a_ele.get('href'))
            except Exception as e:
                LOGGER.warning(f'''
                    Print element not found for {recipe_result_url}. \
                    Using {recipe_result_url} as print URL. . .
                ''')

        return recipe_print_urls
