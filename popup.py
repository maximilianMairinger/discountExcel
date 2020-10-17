from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
from upoi import *
from ob import *
from promise import Promise



def inquire(quest: str, parent, title = None):
  if title == None:
    title = quest
  

  def inq(res, rej):
    dia = QDialog(parent)
    dia.setWindowTitle(title)
    dia.setFixedWidth(500)
    dia.setFixedHeight(200)

    box = QVBoxLayout()
    dia.setLayout(box)
    box.addWidget(QLabel(quest))
    inputBoxContainer = QtWidgets.QWidget()
    inputBox = QHBoxLayout()
    inputBoxContainer.setLayout(inputBox)
    box.addWidget(inputBoxContainer)
    inputField = QLineEdit()
    
    inputBox.addWidget(inputField)
    confButton = QPushButton("Confirm")
    inputBox.addWidget(confButton)
    
    

    def click(): 
      res(inputField.text())
      dia.hide()
    
    confButton.clicked.connect(click)

    def blurElem(elems, fn): 
      def f(e = None): 
        foc = False
        for elem in elems:
          if elem.hasFocus(): 
            foc = True
        
        if not foc: 
          fn()
          
      for elem in elems:
        elem.focusOutEvent = f
        
      


    def blur(): 
      rej(Exception("blur"))
      dia.hide()

    blurElem([confButton, inputField], blur)
    
    


    dia.show()

  
  return Promise(inq)

