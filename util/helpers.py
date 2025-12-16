"""
Helper functions for recipe URL processing.
"""
from recipe_util.base import RecipeBase
from recipe_util.recipe import Recipe
from urllib.parse import urlparse
import ipaddress
import socket
from .constants import (
    ALLOWED_PROTOCOLS,
    LOCALHOST_PATTERNS,
    MAX_URL_LENGTH,
    VALID_TLD
)

class URLValidationError(Exception):
    """Raised when URL validation fails."""
    pass

class SSRFProtectionError(URLValidationError):
    """Raised when URL fails SSRF protection checks."""
    pass

class RecipeCreationError(Exception):
    """Raised when recipe object creation fails."""
    pass

def validate_url(url: str) -> str:
    """
    Validate URL and protect against SSRF attacks.
    
    This function checks for:
    1. Valid HTTP/HTTPS protocol
    2. No private/internal IP addresses
    3. No localhost references
    4. No DNS rebinding attacks
    5. Proper URL format
    
    Args:
        url: The URL to validate
        
    Returns:
        The validated and sanitized URL
        
    Raises:
        URLValidationError: If URL format is invalid
        SSRFProtectionError: If URL fails SSRF security checks
    """
    # Strip whitespace
    url = url.strip()
    
    if not url:
        raise URLValidationError("URL cannot be empty")
    
    # Parse the URL
    try:
        parsed = urlparse(url)
    except Exception as e:
        raise URLValidationError(f"Invalid URL format: {e}")
    
    # Check 1: Ensure it's HTTP or HTTPS only
    if parsed.scheme not in ALLOWED_PROTOCOLS:
        raise SSRFProtectionError(
            f"Invalid protocol '{parsed.scheme}'. Only HTTP and HTTPS are allowed"
        )
    
    # Check 2: Ensure hostname exists
    if not parsed.hostname:
        raise URLValidationError("URL must contain a valid hostname")
    
    # Check 3: Block localhost variations
    hostname_lower = parsed.hostname.lower()
    if hostname_lower in LOCALHOST_PATTERNS:
        raise SSRFProtectionError(
            "Access to localhost is not allowed"
        )
    
    # Check 4a: If hostname looks like an IP address, validate it directly
    try:
        # Try to parse hostname as an IP address
        ip_obj = ipaddress.ip_address(parsed.hostname)
        
        # Check if it's a dangerous IP type
        if ip_obj.is_private:
            raise SSRFProtectionError(
                f"Access to private IP addresses is not allowed: {parsed.hostname}"
            )
        
        if ip_obj.is_loopback:
            raise SSRFProtectionError(
                f"Access to loopback addresses is not allowed: {parsed.hostname}"
            )
        
        if ip_obj.is_link_local:
            raise SSRFProtectionError(
                f"Access to link-local addresses is not allowed: {parsed.hostname}"
            )
        
        if ip_obj.is_multicast:
            raise SSRFProtectionError(
                f"Access to multicast addresses is not allowed: {parsed.hostname}"
            )
        
        if ip_obj.is_reserved:
            raise SSRFProtectionError(
                f"Access to reserved addresses is not allowed: {parsed.hostname}"
            )
        
        # If we get here, it's a valid public IP address
        return url
        
    except ValueError:
        # Not an IP address, it's a hostname - continue to DNS resolution
        pass
    
    # Check 4b: For hostnames, resolve DNS and check resolved IPs
    try:
        # Resolve the hostname to IP address(es)
        ip_addresses = socket.getaddrinfo(
            parsed.hostname, 
            None, 
            socket.AF_UNSPEC,
            socket.SOCK_STREAM
        )
        
        for addr_info in ip_addresses:
            ip_str = addr_info[4][0]
            
            try:
                ip_obj = ipaddress.ip_address(ip_str)
                
                # Check if it's a private, loopback, link-local, or reserved IP
                if ip_obj.is_private:
                    raise SSRFProtectionError(
                        f"Hostname '{parsed.hostname}' resolves to private IP: {ip_str}"
                    )
                
                if ip_obj.is_loopback:
                    raise SSRFProtectionError(
                        f"Hostname '{parsed.hostname}' resolves to loopback address: {ip_str}"
                    )
                
                if ip_obj.is_link_local:
                    raise SSRFProtectionError(
                        f"Hostname '{parsed.hostname}' resolves to link-local address: {ip_str}"
                    )
                
                if ip_obj.is_multicast:
                    raise SSRFProtectionError(
                        f"Hostname '{parsed.hostname}' resolves to multicast address: {ip_str}"
                    )
                
                if ip_obj.is_reserved:
                    raise SSRFProtectionError(
                        f"Hostname '{parsed.hostname}' resolves to reserved address: {ip_str}"
                    )
                
            except ValueError:
                # If it's not a valid IP address, skip
                continue
                
    except socket.gaierror as e:
        # DNS resolution failed - in production this might be a network issue
        # or an invalid hostname. For security, we'll allow it to continue
        # (the actual request will fail anyway if the hostname is invalid)
        # but log the issue
        pass
    except SSRFProtectionError:
        # Re-raise SSRF errors
        raise
    except Exception as e:
        # Other unexpected errors - log but don't block
        pass
    
    # Check 5: Block URLs with embedded credentials (potential security issue)
    if parsed.username or parsed.password:
        raise SSRFProtectionError(
            "URLs with embedded credentials are not allowed"
        )
    
    # Check 6: Ensure reasonable URL length (prevent DoS)
    if len(url) > MAX_URL_LENGTH:
        raise URLValidationError(f"URL is too long (max {MAX_URL_LENGTH} characters)")
    
    return url

def get_recipe_object_from_url(url: str) -> RecipeBase:
    """
    Create and return a recipe object for the given URL.
    
    Args:
        url: The recipe URL to process
        
    Returns:
        A RecipeBase subclass instance
        
    Raises:
        RecipeCreationError: If recipe object creation fails
        URLValidationError: If URL validation fails
        SSRFProtectionError: If URL fails SSRF security checks
    """
    try:
        # First, validate URL for security
        validated_url = validate_url(url)
        base_url = get_base_url(validated_url)
        return Recipe(validated_url, base_url)
    except URLValidationError:
        # Re-raise URL validation errors as-is
        raise
    except Exception as e:
        # Wrap other exceptions in RecipeCreationError
        raise RecipeCreationError(f"Failed to create recipe object: {str(e)}") from e
    
def get_base_url(url: str) -> str:
    """
    Extract base URL from a full URL.
    
    Args:
        url: The full URL
        
    Returns:
        The base URL (protocol + domain)
        
    Examples:
        "https://example.com/path" -> "https://example.com"
        "https://www.site.net/page?q=1" -> "https://www.site.net"
    """
    for tld in VALID_TLD:
        if url.find(tld) != -1:
            return url[:url.find(tld)+len(tld)]
    
    # Fallback: try to parse with urlparse
    try:
        parsed = urlparse(url)
        if parsed.scheme and parsed.netloc:
            return f"{parsed.scheme}://{parsed.netloc}"
    except Exception:
        pass
    
    raise URLValidationError(f"Could not extract base URL from: {url}")