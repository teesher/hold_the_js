from django.shortcuts import render
import logging
from search.util.recipe_search_once_upon_a_chef import RecipeSearchOnceUponAChef

LOGGER = logging.getLogger(__name__)

once_upon_a_chef_config = {
    "base_url": "https://www.onceuponachef.com",
    "base_url_search_path": "/search/"
}

# Create your views here.
def home(request):
    LOGGER.info(request.POST)
    if request.POST:
        recipe_search_val = request.POST.get('recipe_search')
        once_upon_a_chef_search = RecipeSearchOnceUponAChef(once_upon_a_chef_config)
        recipe_urls = once_upon_a_chef_search.recipe_search(recipe_search_val)
        render_context = {
            "recipe_urls": recipe_urls,
            "recipe_search_val": recipe_search_val
        }
        return render(request, "home.html", render_context)

    return render(request, "home.html")