from flask import Flask, redirect, jsonify
import logging
from recipe_util.recipe import Recipe
from util.helpers import get_recipe_object_from_url, URLValidationError, RecipeCreationError

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
    
    try:
        recipe_object: Recipe = get_recipe_object_from_url(url)
        print_url = recipe_object.get_recipe_print_url()
        return redirect(print_url, code=302)
    except (URLValidationError, RecipeCreationError) as e:
        logger.warning(f"Invalid URL: {url[:100]} - Error: {str(e)}")
        return jsonify({
            "error": "url not supported or invalid",
            "details": str(e)
        }), 400
    except Exception as e:
        logger.error(f"Unexpected error processing URL: {url[:100]} - Error: {str(e)}")
        return jsonify({
            "error": "internal server error"
        }), 500