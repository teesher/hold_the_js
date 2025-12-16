"""
Security tests for URL validation and SSRF protection.

Run with: python -m tests.test_security
"""
import sys
from pathlib import Path

# Add parent directory to path to allow imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from util.helpers import validate_url, URLValidationError, SSRFProtectionError

def test_valid_urls():
    """Test that valid URLs pass validation."""
    print("Testing valid URLs...")
    valid_urls = [
        "https://www.onceuponachef.com/recipes/test",
        "https://www.allrecipes.com/recipe/123",
        "https://example.com/page",
        "http://www.example.com",
        "https://feelgoodfoodie.net/recipe/pasta",
    ]
    
    for url in valid_urls:
        try:
            result = validate_url(url)
            print(f"  ✓ {url[:60]}")
        except Exception as e:
            print(f"  ✗ {url[:60]} - FAILED: {e}")
    print()

def test_private_ip_protection():
    """Test that private IP addresses are blocked."""
    print("Testing private IP protection...")
    private_ips = [
        "http://192.168.1.1/admin",
        "http://10.0.0.1/internal",
        "http://172.16.0.1/private",
        "https://192.168.0.100/",
    ]
    
    for url in private_ips:
        try:
            validate_url(url)
            print(f"  ✗ {url} - FAILED: Should have been blocked!")
        except SSRFProtectionError as e:
            print(f"  ✓ {url} - Blocked: {str(e)[:60]}")
        except Exception as e:
            print(f"  ~ {url} - Different error: {str(e)[:60]}")
    print()

def test_localhost_protection():
    """Test that localhost references are blocked."""
    print("Testing localhost protection...")
    localhost_urls = [
        "http://localhost/admin",
        "http://127.0.0.1/internal",
        "https://0.0.0.0/service",
        "http://[::1]/api",
    ]
    
    for url in localhost_urls:
        try:
            validate_url(url)
            print(f"  ✗ {url} - FAILED: Should have been blocked!")
        except SSRFProtectionError as e:
            print(f"  ✓ {url} - Blocked: {str(e)[:60]}")
        except Exception as e:
            print(f"  ~ {url} - Different error: {str(e)[:60]}")
    print()

def test_invalid_protocols():
    """Test that non-HTTP(S) protocols are blocked."""
    print("Testing invalid protocol protection...")
    invalid_protocols = [
        "file:///etc/passwd",
        "ftp://ftp.example.com/file",
        "javascript:alert(1)",
        "data:text/html,<script>alert('xss')</script>",
        "gopher://example.com",
    ]
    
    for url in invalid_protocols:
        try:
            validate_url(url)
            print(f"  ✗ {url} - FAILED: Should have been blocked!")
        except SSRFProtectionError as e:
            print(f"  ✓ {url} - Blocked: {str(e)[:60]}")
        except URLValidationError as e:
            print(f"  ✓ {url} - Blocked: {str(e)[:60]}")
    print()

def test_embedded_credentials():
    """Test that URLs with embedded credentials are blocked."""
    print("Testing embedded credentials protection...")
    credential_urls = [
        "http://user:pass@example.com/page",
        "https://admin:secret@site.com/admin",
    ]
    
    for url in credential_urls:
        try:
            validate_url(url)
            print(f"  ✗ {url} - FAILED: Should have been blocked!")
        except SSRFProtectionError as e:
            print(f"  ✓ {url} - Blocked: {str(e)[:60]}")
    print()

def test_malformed_urls():
    """Test that malformed URLs are rejected."""
    print("Testing malformed URL protection...")
    malformed_urls = [
        "",
        "not-a-url",
        "http://",
        "https://",
        "://example.com",
    ]
    
    for url in malformed_urls:
        try:
            validate_url(url)
            print(f"  ✗ '{url}' - FAILED: Should have been blocked!")
        except URLValidationError as e:
            print(f"  ✓ '{url}' - Blocked: {str(e)[:60]}")
    print()

def test_url_length():
    """Test that overly long URLs are rejected."""
    print("Testing URL length protection...")
    long_url = "https://example.com/" + "a" * 3000
    
    try:
        validate_url(long_url)
        print(f"  ✗ Long URL - FAILED: Should have been blocked!")
    except URLValidationError as e:
        print(f"  ✓ Long URL ({len(long_url)} chars) - Blocked: {str(e)}")
    print()

def main():
    """Run all security tests."""
    print("=" * 70)
    print("SECURITY VALIDATION TESTS")
    print("=" * 70)
    print()
    
    test_valid_urls()
    test_private_ip_protection()
    test_localhost_protection()
    test_invalid_protocols()
    test_embedded_credentials()
    test_malformed_urls()
    test_url_length()
    
    print("=" * 70)
    print("Testing complete!")
    print("=" * 70)

if __name__ == "__main__":
    main()

