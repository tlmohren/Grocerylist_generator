import shoplist
import yaml
import os
import glob 
import shoplist.cooking_functions as cf

def main():
    file_config = "config.yml"
    with open(file_config) as file_config:
        config_dict = yaml.load(file_config)
 

    if config_dict['log_remote'] == True:
        log_dir = config_dict['remote_dir']  

    searchstr = '' 
    recipes_all =  glob.glob('recipes/*/*.json' )
   

    dish_str = config_dict['week_dishes']

    # print(dish_str.split('\n'))
    select_recipes = dish_str.split('\n')

    output_shopping_file = log_dir + "\\shopping_list.txt"  
    other_grocery_file = log_dir + "\\other_groceries.json"  
    pantry_file = log_dir+ "\\pantry.json"


    shopping_recipes = select_recipes + [other_grocery_file]  # add grocery list not related to recipes

    cf.generate_shoppinglist( output_shopping_file, shopping_recipes, pantry_file ) 
 
if __name__ == "__main__":
    main()
