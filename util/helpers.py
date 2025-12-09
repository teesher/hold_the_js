"""
Helper functions for recipe URL processing.
"""
from typing import Optional, Type
from recipe_util.base import RecipeBase
from .constants import URL_PREFIX_TO_CLASS

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
        base_url = get_base_url(validated_url)
        return recipe_class(validated_url, base_url)
    except URLValidationError:
        return None
    except Exception:
        return None
    
def get_base_url(url: str) -> str:
    """
    generate base url for given url
    """
    valid_tld = [".com", ".net"]
    for tld in valid_tld:
        if url.find(tld) != -1:
            return url[:url.find(tld)+4]

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