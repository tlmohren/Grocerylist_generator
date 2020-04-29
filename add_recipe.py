from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtCore import QUrl
import sys 
import json

class RecipeEditor(QtWidgets.QMainWindow):
    def __init__(self):
        super(RecipeEditor, self).__init__()
        uic.loadUi("add_recipe_gui.ui",self)  

        self.actionOpen.triggered.connect(self.fileOpen)
        self.actionSave.triggered.connect(self.fileSave)
        self.actionExit.triggered.connect(self.fileExit)
 
    def convert_list_to_str( list_str):
        out_str = ''
        for item in list_str:
            if out_str=='':
                out_str=item
            else:
                out_str = out_str+', ' + item
        return out_str

    def convert_list_to_str_lines( list_str):
        out_str = ''
        for item in list_str:
            if out_str=='':
                out_str=item
            else:
                out_str = out_str+'\n' + item
        return out_str

    def line_text_to_string_list(text_in):
        list_steps =[]
        for line in text_in.splitlines():
            list_steps.append(line) 
        return list_steps

    def word_text_to_string_list(text_in):
        list_steps =[]
        for word in text_in.split(','):
            list_steps.append(word.strip()) 
        return list_steps   

    def fileOpen(self): 

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog   # use Qt style if not uncommented 
 

        fileName, _ = QFileDialog.getOpenFileName(self,
            "QFileDialog.getOpenFileName()","", "Json Files (*.json)", options = options) 

        if fileName:  
            with open(fileName) as json_file:
                data = json.load(json_file)

            self.lineEditRecipe.setText( data.get('Name','NA' ) )
            self.lineEditCookingTime.setText( str(data.get('Cooking time',0) ))
            self.lineEditServings.setText( str(data.get('Servings',0) )) 
            self.textEditDescription.setText(data.get('Description','NA') ) 

            ingredient_dict = data.get('Ingredients','NA')

            if ingredient_dict == 'NA':
                dairy_list = ''
                meat_list = ''
                spices_list = ''
                produce_list = ''
                other_list = '' 
            else:
                dairy_list = RecipeEditor.convert_list_to_str( ingredient_dict.get('Dairy','NA') )
                other_list = RecipeEditor.convert_list_to_str( ingredient_dict.get('Other','NA') )
                meat_list = RecipeEditor.convert_list_to_str( ingredient_dict.get('Meat','NA') )
                spices_list = RecipeEditor.convert_list_to_str( ingredient_dict.get('Spices','NA') )
                produce_list = RecipeEditor.convert_list_to_str( ingredient_dict.get('Produce','NA') )
  
            self.textEditDairy.setText(dairy_list) 
            self.textEditMeat.setText(meat_list) 
            self.textEditProduce.setText(produce_list) 
            self.textEditSpices.setText(spices_list) 
            self.textEditOther.setText(other_list) 

            self.textEditSteps.setText( RecipeEditor.convert_list_to_str_lines(data['Steps']) ) 
            self.textEditNotes.setText( RecipeEditor.convert_list_to_str_lines(data['Notes']) ) 
 
    def fileSave(self): 
 

        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog   # use Qt style if not uncommented
        fileName, _ = QFileDialog.getSaveFileName(self,
            "QFileDialog.getSaveFileName()","", "Json Files (*.json)", options = options) 

        if fileName: 
            recipe_dict={}
       
            recipe_dict['Name'] = self.lineEditRecipe.text() 
            recipe_dict['Cooking time'] = int(self.lineEditCookingTime.text() ) 
            recipe_dict['Servings'] = int(self.lineEditServings.text() )
            recipe_dict['Description'] = self.textEditDescription.toPlainText() 
   
            ingredients_dict = {} 
            ingredients_dict['Produce'] = RecipeEditor.word_text_to_string_list( self.textEditProduce.toPlainText()  )
            ingredients_dict['Dairy'] = RecipeEditor.word_text_to_string_list( self.textEditDairy.toPlainText()  )
            ingredients_dict['Meat'] = RecipeEditor.word_text_to_string_list( self.textEditMeat.toPlainText()  )
            ingredients_dict['Spices'] = RecipeEditor.word_text_to_string_list( self.textEditSpices.toPlainText()  )
            ingredients_dict['Other'] = RecipeEditor.word_text_to_string_list( self.textEditOther.toPlainText()  )

            recipe_dict['Ingredients'] = ingredients_dict
   
            recipe_dict['Steps'] = RecipeEditor.line_text_to_string_list( self.textEditSteps.toPlainText()  )
            recipe_dict['Notes'] = RecipeEditor.line_text_to_string_list( self.textEditNotes.toPlainText()  )

            with open(fileName+'.json', 'w') as outfile:
                json.dump(recipe_dict , outfile, indent=2)

    def fileExit(self):
        QtWidgets.QApplication.quit()

app = QtWidgets.QApplication([])
win = RecipeEditor()
win.show()
sys.exit(app.exec())