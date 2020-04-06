# Shopping list generator

To get started:
* look if <code>pylatex</code>  is installed correctly (if not, you can skip pdf generation)
* open <code>pantry.json</code> , and add items in your pantry (spices e.g.)
* open <code>other_groceries.json</code> to add items not related to the recipes to your grocery list
* open and run <code>Generate_recipes_shoppinglist.ipynb</code>

Running the jupyter notebook <code>Generate_recipes_shoppinglist.ipynb</code>  will allow one to select recipes. Subsequently the notebook will look through <code>pantry.json</code>  and <code>other_groceries.json</code>  to generate:
- <code>shopping_list.txt</code>
- <code>weekly_recipes.pdf</code>

The script to generate <code> weekly_recipes.pdf</code>  requires <code> pylatex </code> to be installed correctly, which relies on pearl. If you don't have <code> pylatex</code>  installed, there is the option to skip the pdf generation. You can find the recipes in the <code> .json</code>  formats in the subfolders, e.g. dinner -> <code>lasagna.json</code> .

## Suggestions on how to use this script  
For me, I have started logging recipes I've tried in json files. I then select a few recipes every week and set the output folder to my dropbox. This syncs to the dropbox app on my phone, so I can access the recipe and shopping list away from my laptop.


## under construction
* error messages
* adding new recipes  
* layout of weekly recipes
* more robust code
