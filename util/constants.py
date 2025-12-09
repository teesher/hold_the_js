from typing import Type
from recipe_util.base import RecipeBase
from recipe_util.once_upon_a_chef import RecipeOnceUponAChef
from recipe_util.salt_and_lavender import RecipeSaltAndLavender
from recipe_util.all_recipes import RecipeAllRecipes
from recipe_util.cooking_with_ayeh import RecipeCookingWithAyeh
from recipe_util.culinary_hill import RecipeCulinaryHill
from recipe_util.eat_with_clarity import RecipeEatWithClarity
from recipe_util.feel_good_foodie import RecipeFeelGoodFoodie

# Map URL prefixes to their corresponding recipe classes
URL_PREFIX_TO_CLASS: dict[str, Type[RecipeBase]] = {
    'https://www.onceuponachef.com': RecipeOnceUponAChef,
    'https://www.saltandlavender.com': RecipeSaltAndLavender,
    'https://www.allrecipes.com': RecipeAllRecipes,
    'https://eatwithclarity.com': RecipeEatWithClarity,
    'https://www.culinaryhill.com': RecipeCulinaryHill,
    'https://cookingwithayeh.com': RecipeCookingWithAyeh,
    'https://feelgoodfoodie.net': RecipeFeelGoodFoodie,
}