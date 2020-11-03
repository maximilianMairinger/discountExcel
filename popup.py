from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
from upoi import *
from ob import *
from promise import Promise
from typing import *
import re 
from threading import Timer



def constructAllowRegex(regex): 
  def allowRegex(s: str):
    return not not re.search(regex, s)

  return allowRegex

allowEmail = constructAllowRegex('^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$')
allowUrl = constructAllowRegex('^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?$')
allowSignedNumber = constructAllowRegex('^(-|\+|)\d*(.|)\d\d*$')
allowUnsignedNumber = constructAllowRegex('^(\+|)\d*(.|)\d\d*$')
allowSignedInt = constructAllowRegex('^(-|\+|)\d\d*$')
allowUnsignedInt = constructAllowRegex('^(\+|)\d\d*$')


def allAllowed(s: str): 
  return True

def inquire(quest: str, kind: Union[Callable, str] = allAllowed, parent = None, title = None):
  if isinstance(kind, QtWidgets.QWidget): 
    parent = kind
    kind = allAllowed
  else:
    if isinstance(kind, str): 
      if kind == "text" or kind == "txt" or kind == "any" or kind == "":
        kind = allAllowed
      if kind == "number" or kind == "signedNumber" or kind == "num" or kind == "singedNum" or kind == "+/-num" or kind == "+/-number": 
        kind = allowSignedNumber
      elif kind == "unsignedNumber" or kind == "unsignedNum" or kind == "+num" or kind == "+number":
        kind = allowUnsignedNumber
      elif kind == "int" or kind == "integer" or kind == "signedInt" or kind == "signedInteger" or kind == "+/-int" or kind == "+/-integer": 
        kind = allowSignedInt
      elif kind == "unsignedInteger" or kind == "unsignedInt" or kind == "+int" or kind == "+integer":
        kind = allowUnsignedInt
      elif kind == "email":
        kind = allowEmail
      elif kind == "url":
        kind = allowUrl
    



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

    inputField.setStyleSheet("color: red;")
    

    valid = False


    cancelCurrentToggle = None
    def confirm(): 
      nonlocal valid
      nonlocal cancelCurrentToggle

      if valid: 
        res(inputField.text())
        dia.hide()
      else: 
        
        if cancelCurrentToggle != None: 
          cancelCurrentToggle()
          
        toggleBool = True
        times = 5

        def toggle(): 
          nonlocal toggleBool
          nonlocal cancelCurrentToggle
          nonlocal times
          

          times = times - 1
          
          if toggleBool: 
            inputField.setStyleSheet("background: red; color: white;")
          else: 
            inputField.setStyleSheet("background: white; color: red;")
          
          toggleBool = not toggleBool
          if times >= 0:
            t = Timer(.3, toggle)
            def cancTimer():
              nonlocal t
              t.cancel()
            cancelCurrentToggle = cancTimer
            t.start()
          else: 
            cancelCurrentToggle = None
            


        toggle()


    confButton.clicked.connect(confirm)
    

    def onValueChange(): 
      nonlocal valid
      nonlocal cancelCurrentToggle
      if cancelCurrentToggle != None:
        cancelCurrentToggle()

      txt = inputField.text()
      valid = kind(txt)
      if valid: 
        inputField.setStyleSheet("color: black;")
      else: 
        inputField.setStyleSheet("color: red;")

    onValueChange()
    
      
    
    inputField.textChanged.connect(onValueChange)
          
    
    


    

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
        
      


    def cancel(): 
      nonlocal cancelCurrentToggle
      if cancelCurrentToggle != None:
        cancelCurrentToggle()
      rej(Exception("blur"))
      dia.hide()

    blurElem([confButton, inputField], cancel)
    
    


    dia.show()

  
  return Promise(inq)

