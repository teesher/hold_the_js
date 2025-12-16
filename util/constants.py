# HTTP Request Headers
REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

# URL Validation Constants
ALLOWED_PROTOCOLS = ['http', 'https']

LOCALHOST_PATTERNS = [
    'localhost',
    '0.0.0.0',
    '0000:0000:0000:0000:0000:0000:0000:0001',
    '0000:0000:0000:0000:0000:0000:0000:0000',
    '::1',
    '::',
]

MAX_URL_LENGTH = 2048

VALID_TLD = [".com", ".net", ".org"]