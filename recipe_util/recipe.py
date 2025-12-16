from .base import RecipeBase
from bs4 import BeautifulSoup as bs
import re
import logging

LOGGER = logging.getLogger(__name__)

class Recipe(RecipeBase):
    """
    Generic recipe handler that tries multiple strategies to find the print URL.
    
    Strategies (in order):
    1. Check for WordPress Recipe Maker (WPRM) plugin
    2. Search for print button/link in HTML
    3. Try common query parameter patterns
    4. Fall back to original URL
    """
    
    def _get_recipe_print_url(self, url: str, soup: bs):
        """
        Try multiple strategies to find the recipe print URL.
        
        Args:
            url: The original recipe URL
            soup: BeautifulSoup object of the page
            
        Returns:
            The print URL (or original URL if none found)
        """
        
        # Strategy 1: Check for WPRM plugin
        wprm_url = self._try_wprm_plugin(soup)
        if wprm_url:
            LOGGER.info(f"Found WPRM print URL: {wprm_url}")
            return wprm_url
        
        # Strategy 2: Search for print button/link
        print_link = self._try_find_print_link(soup)
        if print_link:
            LOGGER.info(f"Found print link in HTML: {print_link}")
            return print_link
        
        # Strategy 3: Try common query parameter patterns
        query_param_url = self._try_common_patterns(url, soup)
        if query_param_url:
            LOGGER.info(f"Found print URL via query pattern: {query_param_url}")
            return query_param_url
        
        # Strategy 4: Fall back to original URL
        LOGGER.warning(f"No print URL found for {url}, returning original")
        return url
    
    def _try_wprm_plugin(self, soup: bs) -> str | None:
        """
        Check if the site uses WordPress Recipe Maker (WPRM) plugin.
        
        WPRM indicators:
        - Links containing 'wprm_print'
        - Elements with 'wprm-' class prefixes
        - Recipe containers with WPRM IDs
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            WPRM print URL if found, None otherwise
        """
        # Look for links with wprm_print in href
        wprm_links = soup.find_all("a", href=re.compile(r"/wprm_print/"))
        if wprm_links:
            href = wprm_links[0].get("href")
            if href:
                LOGGER.debug(f"Found WPRM link: {href}")
                return href
        
        # Look for WPRM print button by class
        wprm_print_button = soup.find("a", class_="wprm-recipe-print")
        if wprm_print_button:
            href = wprm_print_button.get("href")
            if href:
                LOGGER.debug(f"Found WPRM print button: {href}")
                return href
        
        # Check if WPRM recipe container exists, then construct URL
        wprm_container = soup.find(class_=re.compile(r"wprm-recipe-container"))
        if wprm_container:
            # Try to construct WPRM URL manually
            # WPRM URLs typically follow pattern: /wprm_print/[post-id]
            recipe_id = wprm_container.get("data-recipe-id")
            if recipe_id:
                wprm_url = f"{self.base_url}/wprm_print/{recipe_id}"
                LOGGER.debug(f"Constructed WPRM URL from recipe ID: {wprm_url}")
                return wprm_url
        
        return None
    
    def _try_find_print_link(self, soup: bs) -> str | None:
        """
        Search for print button or link in the HTML.
        
        Looks for:
        - <a> tags with 'print' in class name
        - <a> tags with 'print' in href
        - <button> with print icon or text
        - Links with common print URL patterns
        
        Args:
            soup: BeautifulSoup object
            
        Returns:
            Print link URL if found, None otherwise
        """
        # Strategy 1: Look for links with 'print' in class
        print_class_links = soup.find_all("a", class_=re.compile(r"print", re.IGNORECASE))
        for link in print_class_links:
            href = link.get("href")
            if href and self._is_valid_print_url(href):
                LOGGER.debug(f"Found print link by class: {href}")
                return href
        
        # Strategy 2: Look for links with 'print' in href
        print_href_links = soup.find_all("a", href=re.compile(r"print", re.IGNORECASE))
        for link in print_href_links:
            href = link.get("href")
            if href and self._is_valid_print_url(href):
                LOGGER.debug(f"Found print link by href: {href}")
                return href
        
        # Strategy 3: Look for links with print-related text
        all_links = soup.find_all("a")
        for link in all_links:
            text = link.get_text(strip=True).lower()
            if "print" in text:
                href = link.get("href")
                if href and self._is_valid_print_url(href):
                    LOGGER.debug(f"Found print link by text: {href}")
                    return href
        
        return None
    
    def _is_valid_print_url(self, url: str) -> bool:
        """
        Check if a URL looks like a valid print URL.
        
        Args:
            url: URL to check
            
        Returns:
            True if it looks like a print URL, False otherwise
        """
        if not url:
            return False
        
        # Avoid javascript: and other non-http protocols
        if url.startswith(("javascript:", "mailto:", "#")):
            return False
        
        # Should contain 'print' somewhere
        if "print" not in url.lower():
            return False
        
        return True
    
    def _try_common_patterns(self, url: str, soup: bs) -> str | None:
        """
        Try common query parameter patterns for print URLs.
        
        Patterns tried:
        - ?recipe_print=yes
        - ?print=
        - ?print
        - /print/
        
        Args:
            url: Original URL
            soup: BeautifulSoup object (to verify pattern exists in HTML)
            
        Returns:
            Print URL if pattern found in page source, None otherwise
        """
        # Common patterns to try
        patterns = [
            f"{url}?recipe_print=yes",
            f"{url}?print=",
            f"{url}?print",
            f"{url}/print/",
        ]
        
        # Check if any pattern appears in the page source
        page_text = soup.get_text()
        for pattern in patterns:
            # Check if this pattern or similar exists in the HTML
            if "recipe_print" in page_text or "?print" in str(soup):
                LOGGER.debug(f"Found print pattern in HTML, trying: {pattern}")
                return pattern
        
        return None

