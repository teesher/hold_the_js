import abc
import logging
from .recipe_base import Recipe
from urllib.parse import quote
import requests
from bs4 import BeautifulSoup as bs
from core.settings import VERBOSE

LOGGER = logging.getLogger(__name__)

STATUS_CODE_OK = 200
DEFAULT_TIMEOUT = 300

class RecipeSearchBase():
    def __init__(self, config):
        self._base_url = config.get("base_url")
        self._base_url_search_path = config.get("base_url_search_path") 
        self._search_soup = None

    def recipe_search(self, search_string):
        recipes = []

        # Retrieve HTML and put in bs4 object to save time / requests
        self._save_search_html_requests(search_string)

        # Retrieve recipe URLs from bs4 object
        recipe_result_urls = self._get_recipe_result_urls()

        if VERBOSE:
            for recipe_result_url in recipe_result_urls:
                LOGGER.info(f"Found recipe result URL: {recipe_result_url}")

        # Retrieve recipe names from bs4 object
        recipe_names = self._get_recipe_names()

        if VERBOSE:
            for recipe_name in recipe_names:
                LOGGER.info(f"Found recipe name: {recipe_name}")

        # Retrieve recipe images from bs4 object
        recipe_image_urls = self._get_recipe_image_urls()

        if VERBOSE:
            for recipe_image_url in recipe_image_urls:
                LOGGER.info(f"Found recipe image URL: {recipe_image_url}")

        # Retrieve print URLs from recipe URLs
        recipe_print_urls = self._get_recipe_print_urls(recipe_result_urls)

        for recipe_name, recipe_print_url, recipe_image_url in zip(recipe_names, recipe_print_urls, recipe_image_urls):
            recipes.append(self._generate_recipe_object(recipe_name, recipe_print_url, recipe_image_url))

        # return []
        return recipes
    
    def _generate_recipe_object(self, recipe_name, recipe_url, recipe_image_url):
        return Recipe(
            title=recipe_name,
            url=recipe_url,
            image_url = recipe_image_url
        )
    
    def _retrieve_soup_from_url(self, url):
        response = requests.get(url=url, timeout=DEFAULT_TIMEOUT)
        if response.status_code == STATUS_CODE_OK:
            return bs(response.text, "html.parser")
        else:
            # TODO set up django error handling
            LOGGER.error("Bad request")

    def _save_search_html_requests(self, search_string: str):
        self._search_soup = self._retrieve_soup_from_url(
            self._base_url + self._base_url_search_path + quote(search_string)
        )

    @abc.abstractmethod
    def _get_recipe_result_urls(self):
        raise NotImplementedError()
    
    @abc.abstractmethod
    def _get_recipe_print_urls(self, recipe_result_urls):
        raise NotImplementedError()
    
    @abc.abstractmethod
    def _get_recipe_names(self):
        raise NotImplementedError()
    
    @abc.abstractmethod
    def _get_recipe_image_urls(self):
        raise NotImplementedError()

