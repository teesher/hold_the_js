# Hold the JS
in progress. 

take the js out of your recipes.

## usage
edit the recipe url you are on so that you pass the url as an arg to hold the js.

## example
if you are on `https://www.bloat-recipe.com/another-bloated-recipe`

change url to: `https://www.hold-the-js.xyz/https://www.bloat-recipe.com/another-bloated-recipe`

## how it works
1. url of recipe as param is validated in app.py and recipe site specific class object is instantiated
2. print url is retrieved in way that is specific to that recipe site
3. user redirected to print url

### supported domains
1. `https://www.onceuponachef.com`
2. `https://www.saltandlavender.com`
3. `https://www.allrecipes.com`

### domains in progress
