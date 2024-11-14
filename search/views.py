from django.shortcuts import render
import logging
from search.util.recipe_search_once_upon_a_chef import RecipeSearchOnceUponAChef
from search.util.recipe_search_salt_and_lavender import RecipeSearchSaltAndLavender
from core.settings import VERBOSE

LOGGER = logging.getLogger(__name__)

once_upon_a_chef_config = {
    "base_url": "https://www.onceuponachef.com",
    "base_url_search_path": "/search/"
}

salt_and_lavender_config = {
    "base_url": "https://www.saltandlavender.com",
    "base_url_search_path": "/?s="
}

# Create your views here.
def home(request):
    LOGGER.info(request.POST)

    if request.POST:
        recipe_search_val = request.POST.get('recipe_search')
        recipe_objects = []

        # Once Upon a Chef
        once_upon_a_chef_search = RecipeSearchOnceUponAChef(once_upon_a_chef_config)
        recipe_objects.extend(once_upon_a_chef_search.recipe_search(recipe_search_val))
        
        # Salt and Lavender
        salt_and_lavender_search = RecipeSearchSaltAndLavender(salt_and_lavender_config)
        recipe_objects.extend(salt_and_lavender_search.recipe_search(recipe_search_val))

        if VERBOSE:
            LOGGER.info(f"Found {len(recipe_objects)} recipes")

        render_context = {
            "recipes": recipe_objects,
            "recipe_search_val": recipe_search_val
        }
        return render(request, "home.html", render_context)

    return render(request, "home.html")