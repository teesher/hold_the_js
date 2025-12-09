from flask import Flask, redirect, jsonify
import logging
from recipe_util.base import RecipeBase
from util.helpers import get_recipe_object_from_url

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/<path:url>")
def process_url(url):
    logger.info(f"Processing URL: {url[:100]}")
    
    recipe_object: RecipeBase | None = get_recipe_object_from_url(url)
    
    if recipe_object is None:
        logger.warning(f"Invalid URL: {url[:100]}")
        return jsonify({
            "error": "Invalid URL",
            "message": "url not supported"
        }), 400
    
    try:
        print_url = recipe_object.get_recipe_print_url()
        logger.info(f"Redirecting to: {print_url[:100]}")
        return redirect(print_url, code=302)
    except Exception as e:
        logger.error(f"Error: {e}")
        return jsonify({
            "error": "Failed to process recipe"
        }), 500