from flask import Flask, redirect
from util.recipe_search_once_upon_a_chef import RecipeSearchOnceUponAChef

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/<path:url>")
def process_url(url):
    rs_once_upon_a_chef = RecipeSearchOnceUponAChef(url)
    return redirect(rs_once_upon_a_chef.get_recipe_print_url())