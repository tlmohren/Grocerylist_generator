
import json
from pylatex import Document, Subsection, Itemize, Enumerate, Description, \
    Command, NoEscape, MiniPage, LineBreak, VerticalSpace, Section,  escape_latex, NoEscape, Package
from pylatex.basic import NewLine


def unique(list1): 

    # intilize a null list 
    unique_list = [] 

    # traverse for all elements 
    for x in list1: 
        # check if exists in unique_list or not 
        if x not in unique_list: 
            unique_list.append(x) 
    return unique_list

def hyperlink(url,text):
    text = escape_latex(text)
    return NoEscape(r'\href{' + url + '}{' + text + '}')
          
def create_weeklyCookbook( recipes, output_file ):  

    list_options = { 'itemsep':'0pt','parsep':'0pt','left':'0pt' }  

    geometry_options = {"tmargin": "1cm", "lmargin": "1.5cm", "bmargin": "1cm"}
    doc = Document(geometry_options=geometry_options, page_numbers=False)
    doc.packages.append(Package('hyperref'))
 
    with doc.create(Enumerate(enumeration_symbol=r"\alph*)",
                              options={'start': 20})) as enum: 
        # print('Empty entry to ensure enumitem package is used')
        a = []

    for recipe_loc in recipes:
        print(recipe_loc)
        with open( recipe_loc , 'r') as f:
            recipe_dict = json.load(f)   

        recip_headline = recipe_dict['Name'] + '        (' +  str(recipe_dict['Cooking time']) + ' min)' 
        with doc.create(Subsection( recip_headline ,numbering=False  )):   
  
            with doc.create(MiniPage(width=r"0.3\textwidth")):
                with doc.create(Itemize( options=list_options) ) as itemize: 
                    for item in recipe_dict['Ingredients'].keys(): 
                        if len( recipe_dict['Ingredients'][item] ) > 0: 
    #                         itemize.add_item( recipe_dict['Ingredients'][item] )  
                            for subitem in recipe_dict['Ingredients'][item]:
                                itemize.add_item(subitem) 

                if  len( recipe_dict['Equipment'] ) > 0: 
                    with doc.create(Itemize( options=list_options) ) as itemize: 
                        for item in recipe_dict['Equipment'] : 
                            itemize.add_item(  item )   

            with doc.create(MiniPage(width=r"0.8\textwidth")):
                with doc.create( Enumerate(options=list_options) ) as enum:   
                    for step in recipe_dict['Steps']:
                        enum.add_item( step )     

                with doc.create(Itemize(options=list_options) ) as itemize: 
                    if len(recipe_dict['Notes']) > 0:
                        for item in recipe_dict['Notes']:
                            if len( item ) > 0: 
                                itemize.add_item( item)  

                if recipe_dict.get("Link")  is not None: 


    
                    if type( recipe_dict["Link"] ) == list:
                        link0 =  recipe_dict["Link"][0] 
                    elif type( recipe_dict["Link"] ) == str:
                        link0 =  recipe_dict["Link"] 



                    doc.append( hyperlink( link0 , link0  ) ) 

    doc.generate_pdf( output_file, clean_tex=True) 

 
def generate_shoppinglist(list_loc, recipes, pantry_loc ): 
    file = open( list_loc,"w")  

    with open( pantry_loc , 'r') as f:  
        pantry_dict = json.load(f)   

    shopping_dict= { 'Produce':[],'Dairy':[],'Meat':[],'Spices':[],'Other':[]}
    meal_list = []

    for recipe_loc in recipes: 
        # print(recipe_loc)
        with open( recipe_loc , 'r') as f:  
            recipe_dict = json.load(f)   
            for key in shopping_dict.keys():         
                produce_list =  recipe_dict['Ingredients'][key] 
                shopping_dict[key] =  shopping_dict[key] + produce_list
                
            meal_descrip = recipe_dict["Name"] + ' (' + str(recipe_dict["Servings"] ) + ' srv)'
            meal_list.append( meal_descrip  )
    shopping_dict['Meal']= meal_list 
     
    for key in  ['Meal'] + list( shopping_dict.keys() )[:-1]:   
        key_list = shopping_dict[key]  
        
        key_list = sorted(  key_list, key=str.lower)  
        key_dict = {}  
        for item in key_list: 
            item_only = item.split('(')[0].rstrip().lower() 

            if len(item.split('('))>1:
                quantity = item.split('(')[1].split(')')[0] 
            else:
                quantity = '1x'

            if key == 'Meal': 
                bool_not_in_pantry = True
            else: 
                bool_not_in_pantry = item_only not in pantry_dict[key] 
    
            if (item_only not in key_dict) & bool_not_in_pantry:
                key_dict[item_only] = [quantity] 
            elif bool_not_in_pantry:
                key_dict[item_only].append(quantity)
            else: 
                print( item_only , ' is in the pantry')
      
        for item in key_dict.keys(): 
            quant_str = ' ['
            for its in key_dict[item]:
                quant_str = quant_str+ its + ',' 
            quant_str = quant_str + ']'  
            file.write( item + quant_str + '\n' )
            print( item + quant_str  )
     
        file.write('-----------------\n')
        print('------------------------') 
     
    file.close()   
