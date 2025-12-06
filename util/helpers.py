"""
Helper functions for recipe URL processing.
"""
from typing import Optional
from .recipe_base import RecipeBase
from .recipe_once_upon_a_chef import RecipeOnceUponAChef

ALLOWED_URL_PREFIX = 'https://www.onceuponachef.com'

class URLValidationError(Exception):
    """Raised when URL validation fails."""
    pass

def get_recipe_object_from_url(url: str) -> Optional[RecipeBase]:
    if not url:
        return None
    
    try:
        validated_url = validate_url(url)
        return RecipeOnceUponAChef(validated_url)
    except URLValidationError:
        return None
    except Exception:
        return None

def validate_url(url: str) -> str:
    if not url or not isinstance(url, str):
        raise URLValidationError("URL must be a non-empty string")
    
    url = url.strip()
    
    if not url.startswith(ALLOWED_URL_PREFIX):
        raise URLValidationError(
            f"URL must start with {ALLOWED_URL_PREFIX}"
        )
    
    if len(url) > len(ALLOWED_URL_PREFIX):
        next_char = url[len(ALLOWED_URL_PREFIX)]
        if next_char not in ['/', '?']:
            raise URLValidationError(
                f"Invalid URL format after {ALLOWED_URL_PREFIX}"
            )
    
    return url