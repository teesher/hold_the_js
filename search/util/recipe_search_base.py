import abc
import logging

LOGGER = logging.getLogger(__name__)

STATUS_CODE_OK = 200
DEFAULT_TIMEOUT = 300

class RecipeSearchBase():
    def __init__(self, config):
        self._base_url = config.get("base_url")
        self._base_url_search_path = config.get("base_url_search_path") 

    def recipe_search(self, search_string):
        recipe_result_urls = self._get_recipe_result_urls(search_string)
        recipe_print_urls = self._get_recipe_print_urls(recipe_result_urls)
        return recipe_print_urls

    @abc.abstractmethod
    def _get_recipe_result_urls(search_string):
        raise NotImplementedError()
    
    @abc.abstractmethod
    def _get_recipe_print_urls(recipe_result_urls):
        raise NotImplementedError()

