from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
import sys
from upoi import *
from ob import *
from popup import inquire
import tkinter as tk
from tkinter import filedialog




# poi = UPOI("data/test")
# print(poi.data[2].name)






# for button in self.buttons:
    #   button.clicked.connect(lambda parameter_list: 
    #     self.handelClick(self.sender().id)
    #   )


# Window is the base Widget, used as a Window (below)
# for this application
class Window(QtWidgets.QWidget):

  
  def __init__(self):
    super().__init__()
    # Init Window parameters like title and size
    self.setWindowTitle("Excel")
    self.setGeometry(500, 500, 2000, 1000)

    # A flag if all autosaving features shall be inited. 
    # At this point there is nothing changing this.
    self.autoSave = False

    # Create the base Boxlayout and attach it ti self
    vBoxLayout = QVBoxLayout()
    self.setLayout(vBoxLayout)


    # This gets called when there is a change detected originating from the file
    # The idea was to rerender the complete table. But sadly I get some Multithreading errors
    # and the vBoxLayout#replaceWidget method does not work like thought. 
    def onFileChange():
      print("file originating change")

      nonlocal vBoxLayout
      nonlocal self
      table1 = self.table
      self._createTable()
      table2 = self.table
      vBoxLayout.replaceWidget(table1, table2)
    
    # Only really use it when the autoSave flag is set
    useOnFileChanged = None
    if self.autoSave:
      useOnFileChanged = onFileChange

    
    # Declare and init a UPOI instance which is connected to a specified file.
    # In the future this hardcoded string could be replace by the context in which 
    # this app was called (like double click on a file)

    header = ["Nummer", "Kategorie", "Name", "Icon-Bez", "Latitude", "Longitude", "Länderkennzeichen", "Unbekannt", "Unbekannt 2", "Unbekannt 3", "Postleitzahl", "Ort", "Straße", "Hausnummer", "Information", "Telefonnummer"]
    self.poi = UPOI("data/data", header, useOnFileChanged)
    
    
    

    # Create the main view table with the current UPOI as init data. 
    self._createTable()
    vBoxLayout.addWidget(self.table)


    # Declare and Init other GUI elements
    # Add row and add col Buttons are inited and appended properly here
    addRowButton = QPushButton("Add row")
    addRowButton.clicked.connect(lambda : 
      self.addRow()
    )
    addColButton = QPushButton("Add col")
    addColButton.clicked.connect(lambda : 
      self.addCol()
    )
    
    botBoxContainer = QtWidgets.QWidget()
    botBox = QHBoxLayout()
    botBoxContainer.setLayout(botBox)
    vBoxLayout.addWidget(botBoxContainer)

    # Save Button is inited and appended properly here
    saveButton = QPushButton("Save")
    saveButton.clicked.connect(lambda : 
      self.save()
    )

    # Save Button is inited and appended properly here
    saveAs = QPushButton("Save as")
    def saveAsFunc():
      # Open file dialog; where to save
      root = tk.Tk()
      root.withdraw()
      filePath = filedialog.asksaveasfile().name

      self.poi.file.filePath(filePath)
      self.save()


    saveAs.clicked.connect(saveAsFunc)

    # Save Button is inited and appended properly here
    openButton = QPushButton("Open")
    def openFunc():
      # Open file dialog; where to open
      root = tk.Tk()
      root.withdraw()
      filePath = filedialog.askopenfile().name

      # Set filepath without write
      self.poi.file.filePath(filePath, True)
      # Parse poi again
      self.poi.parse()
      
      # Create table with new POI
      table1 = self.table
      self._createTable()
      table2 = self.table
      vBoxLayout.replaceWidget(table1, table2)

    openButton.clicked.connect(openFunc)


    # Append to buttons to botBox
    botBox.addWidget(addRowButton)
    botBox.addWidget(addColButton)
    botBox.addWidget(saveButton)
    botBox.addWidget(saveAs)
    botBox.addWidget(openButton)


  # Save the current poi to file
  def save(self):
    self.poi.save()

  # Gets called when a row wants to be added by the user
  def addRow(self): 
    # Change the gui table accordingly
    self.table.setRowCount(self.table.rowCount() + 1)
    # Change poi accordingly
    self.poi.data.append(Object())
    # Save to file when autosave flag is set
    if (self.autoSave): 
      self.poi.save()
    
  # Gets called when a col wants to be added by the user
  # Here a column name must be inquired
  def addCol(self): 
    # Gets called when the inquiry is successfully finished by the user
    def then(txt): 
      # get needed data (the col count)
      count = self.table.columnCount()
      # Change the gui table accordingly
      self.table.setColumnCount(count + 1)
      self.table.setHorizontalHeaderItem(count, QTableWidgetItem(txt))
      # Change poi accordingly
      self.poi.types.append(txt)

      # Save to file when autosave flag is set
      if (self.autoSave): 
        self.poi.save()

    # Validator to ensure no column names are added twice
    # This gets called very often, thus we must ensure that 
    # it is very fast.
    def validator(s: str):
      return s not in self.poi.types

    # Ask the user for the col name. When the user cancels the then callback will not be called
    inquire("Column name", validator, self).then(then)

  # This gets called every time a table cell gets changed by the user
  def tableChanged(self, x, y): 
      # Set the according attr into the parsed poi object.
    setattr(self.poi.data[x], self.poi.types[y], self.table.item(x, y).text())

    # Save to file when autosave flag is set
    if (self.autoSave): 
      self.poi.save()

  # Just a helper function to create a new table with the current poi object.
  def _createTable(self): 
    poi = self.poi
    
    self.table = table = QTableWidget()
    table.setColumnWidth(1, 300)

    table.setColumnCount(len(poi.types))
    table.setRowCount(len(poi.data))

    # Set header
    for i in range(len(poi.types)):
      table.setHorizontalHeaderItem(i, QTableWidgetItem(poi.types[i]))

    table.setSortingEnabled(True)


    data = poi.data

    # Set cells
    for x in range(len(data)):
      for y in range(len(poi.types)):
        s = getattr(data[x], poi.types[y])
        q = QTableWidgetItem(s)
        table.setItem(x, y, q)


    # Call table changed when table cell changes
    table.cellChanged.connect(lambda x, y: 
      self.tableChanged(x, y)
    )
    return table
    

        

# Here the Window class (above) gets inited and started as client window
if __name__ == "__main__": 
  app = QtWidgets.QApplication(sys.argv)
  mywidget = Window()
  mywidget.show()
  sys.exit(app.exec_())

