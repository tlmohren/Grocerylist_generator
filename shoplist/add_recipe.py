from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QFont
import sys 
import json

class RecipeEditor(QtWidgets.QMainWindow):
    def __init__(self):
        super(RecipeEditor, self).__init__()
        uic.loadUi("add_recipe_gui.ui",self)  

        self.actionNew.triggered.connect(self.fileNew)
        self.actionOpen.triggered.connect(self.fileOpen)
        self.actionSave.triggered.connect(self.fileSave)
        self.actionExit.triggered.connect(self.fileExit)
        self.fileName_known = ""
    def convert_list_to_str( list_str):
        if list_str:
            out_str = ''
            for item in list_str:
                if out_str=='':
                    out_str=item
                else:
                    out_str = out_str+', ' + item
        else: 
            out_str = None
        return out_str

    def convert_list_to_str_lines( list_str):
        if list_str:
            out_str = ''
            for item in list_str:
                if out_str=='':
                    out_str=item
                else:
                    out_str = out_str+'\n' + item
        else: 
            out_str = None
        return out_str

    def line_text_to_string_list(text_in):
        list_steps =[]
        for line in text_in.splitlines():
            list_steps.append(line) 
        return list_steps

    def word_text_to_string_list(text_in):
        if text_in:
            list_steps =[]
            for word in text_in.split(','):
                list_steps.append(word.strip()) 
        else:
            list_steps = []
        return list_steps   

    def fileNew(self):   

        self.lineEditRecipe.setText( "" )
        self.lineEditCookingTime.setText(""  )
        self.lineEditServings.setText( "") 
        self.textEditDescription.setText(""  ) 

        self.textEditDairy.setText( "") 
        self.textEditMeat.setText( "") 
        self.textEditProduce.setText("" ) 
        self.textEditSpices.setText("") 
        self.textEditOther.setText( "") 

        self.textEditSteps.setText(  "" ) 
        self.textEditNotes.setText( ""  ) 
        self.fileName_known = ""


    def fileOpen(self):  
        options = QFileDialog.Options(QFileDialog.Detail  ) 
 
        self.fileName_open, _ = QFileDialog.getOpenFileName(self,
            "QFileDialog.getOpenFileName()","", "All files (*);;Json Files (*.json)", options = options) 
       
        print( 'opened: ' + self.fileName_open)
        self.fileName_known = self.fileName_open

        if self.fileName_open:  
            with open(self.fileName_open) as json_file:
                data = json.load(json_file)

            self.lineEditRecipe.setText( data.get('Name','NA' ) )
            self.lineEditCookingTime.setText( str(data.get('Cooking time',0) ))
            self.lineEditServings.setText( str(data.get('Servings',0) )) 
            self.textEditDescription.setText(data.get('Description','NA') ) 

            ingredient_dict = data.get('Ingredients','NA')

            if ingredient_dict == 'NA':
                dairy_list = None
                meat_list =None
                spices_list =None
                produce_list = None
                other_list =None
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
        if self.fileName_known == "":
            options = QFileDialog.Options(QFileDialog.Detail) 
            fileName, _ = QFileDialog.getSaveFileName(self,
                "QFileDialog.getSaveFileName()",self.fileName_known, "Json Files (*.json)", options = options) 

            self.fileName_known = fileName

            if fileName: 
                recipe_dict={}
           
                recipe_dict['Name'] = self.lineEditRecipe.text() 
                recipe_dict['Cooking time'] = self.lineEditCookingTime.text() 
                recipe_dict['Servings'] = self.lineEditServings.text() 
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

                with open(fileName , 'w') as outfile:
                    json.dump(recipe_dict , outfile, indent=2)
                print('Saved: ' + fileName)

        else:  
            recipe_dict={}
       
            recipe_dict['Name'] = self.lineEditRecipe.text() 
            recipe_dict['Cooking time'] = self.lineEditCookingTime.text() 
            recipe_dict['Servings'] = self.lineEditServings.text()  
 
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

            with open(self.fileName_known, 'w') as outfile:
                json.dump(recipe_dict , outfile, indent=2)
            print('Saved: ' + self.fileName_known)

    def fileExit(self):
        QtWidgets.QApplication.quit()

app = QtWidgets.QApplication([])
win = RecipeEditor()
win.show()
sys.exit(app.exec())


if __name__ == '__main__':

    app = QtWidgets.QApplication([])
    win = RecipeEditor()
    win.show()
    sys.exit(app.exec()) 