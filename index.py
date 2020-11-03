from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
import sys
from upoi import *
from ob import *
from popup import inquire


# poi = UPOI("data/test")
# print(poi.data[2].name)






# for button in self.buttons:
    #   button.clicked.connect(lambda parameter_list: 
    #     self.handelClick(self.sender().id)
    #   )

class Window(QtWidgets.QWidget):

  def __init__(self):
    super().__init__()
    self.setWindowTitle("Excel")
    self.setGeometry(500, 500, 2000, 1000)


    self.poi = UPOI("data/test")
    vBoxLayout = QVBoxLayout()
    self.setLayout(vBoxLayout)

    self.autoSave = True
    self._createTable()
    vBoxLayout.addWidget(self.table)

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

    botBox.addWidget(addRowButton)
    botBox.addWidget(addColButton)

    
  def addRow(self): 
    self.table.setRowCount(self.table.rowCount() + 1)
    self.poi.data.append(Object())
    

  def addCol(self): 
    def then(txt): 
      count = self.table.columnCount()
      self.table.setColumnCount(count + 1)
      self.table.setHorizontalHeaderItem(count, QTableWidgetItem(txt))
      self.poi.types.append(txt)
      self.poi.save()

    def validator(s: str):
      return s not in self.poi.types
    inquire("Column name", validator, self).then(then)

  def tableChanged(self, x, y): 
    setattr(self.poi.data[x], self.poi.types[y], self.table.item(x, y).text())
    if (self.autoSave): 
      self.poi.save()


  def _createTable(self): 
    poi = self.poi
    
    self.table = table = QTableWidget()
    table.setColumnWidth(1, 300)

    table.setColumnCount(len(poi.types))
    table.setRowCount(len(poi.data))

    for i in range(len(poi.types)):
      table.setHorizontalHeaderItem(i, QTableWidgetItem(poi.types[i]))

    table.setSortingEnabled(True)


    data = poi.data

    for x in range(len(data)):
      for y in range(len(poi.types)):
        s = getattr(data[x], poi.types[y])
        q = QTableWidgetItem(s)
        table.setItem(x, y, q)



    table.cellChanged.connect(lambda x, y: 
      self.tableChanged(x, y)
    )
    return table
    

        


if __name__ == "__main__": 
  app = QtWidgets.QApplication(sys.argv)
  mywidget = Window()
  mywidget.show()
  sys.exit(app.exec_())

