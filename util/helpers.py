"""
Helper functions for recipe URL processing.
"""
from typing import Optional, Type
from .recipe_base import RecipeBase
from .recipe_once_upon_a_chef import RecipeOnceUponAChef
from .recipe_salt_and_lavender import RecipeSaltAndLavender

# Map URL prefixes to their corresponding recipe classes
URL_PREFIX_TO_CLASS: dict[str, Type[RecipeBase]] = {
    'https://www.onceuponachef.com': RecipeOnceUponAChef,
    'https://www.saltandlavender.com': RecipeSaltAndLavender,
}

class URLValidationError(Exception):
    """Raised when URL validation fails."""
    pass

def get_recipe_object_from_url(url: str) -> Optional[RecipeBase]:
    """
    Create and return a recipe object for the given URL.
    
    Args:
        url: The recipe URL to process
        
    Returns:
        A RecipeBase subclass instance, or None if URL is invalid
    """
    try:
        validated_url, recipe_class = validate_url_and_get_recipe_class(url)
        return recipe_class(validated_url)
    except URLValidationError:
        return None
    except Exception:
        return None

def validate_url_and_get_recipe_class(url: str) -> tuple[str, Type[RecipeBase]]:
    """
    Validate URL and return the validated URL along with its recipe class.
    
    Args:
        url: The URL to validate
        
    Returns:
        Tuple of (validated_url, recipe_class)
        
    Raises:
        URLValidationError: If URL doesn't match any allowed prefix
    """
    url = url.strip()
    
    # Find matching prefix
    for prefix, recipe_class in URL_PREFIX_TO_CLASS.items():
        if url.startswith(prefix):
            # Validate character after prefix
            if len(url) > len(prefix):
                next_char = url[len(prefix)]
                if next_char not in ['/', '?']:
                    raise URLValidationError(
                        f"Invalid URL format after {prefix}"
                    )
            return url, recipe_class
    
    # No matching prefix found
    allowed_prefixes = ', '.join(URL_PREFIX_TO_CLASS.keys())
    raise URLValidationError(
        f"URL must start with one of: {allowed_prefixes}"
    )