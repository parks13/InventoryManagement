import sys, csv
from PyQt5 import QtCore, uic, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QTextEdit, \
    QVBoxLayout, QWidget, QFileDialog, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QTextCharFormat, QTextFormat, QTextObjectInterface
from PyQt5.QtCore import QFile, QIODevice, QObject, QSize

# Load the UI file
UIClass, QtBaseClass = uic.loadUiType("InvScreen.ui")

# Class to handle the GUI of the program
class InvGUI(UIClass, QtBaseClass):
    # default class variables
    filePath = ""
    row = 0

    # Constructs the GUI
    def __init__(self):
        UIClass.__init__(self)
        QtBaseClass.__init__(self)
        self.setupUi(self)
        self.setWindowTitle('Inventory Management Program')  # set the title of the program window
        self.setWindowFlag(QtCore.Qt.WindowMinMaxButtonsHint, False)  # disable windows maximize button
        self.setFixedSize(752, 401)  # fix the windows size

        # Show open file page and let the user open csv file and proceed to next page
        self.stackedWidget.setCurrentIndex(0)
        self.openFileButton.clicked.connect(self.OpenFile)

        # Connect cellClicked event to a function displaying its related values
        self.tableWidget.cellClicked.connect(self.ClickedCell)

        # Connect search button to search item name in QTableWidget
        self.searchButton.clicked.connect(self.Search)

        # Connect save button to save new quantity of the item
        self.setNewQuantityButton.clicked.connect(self.ChangeQuantity)

    # Opens a single .csv file
    def OpenFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        InvGUI.filePath = QFileDialog.getOpenFileName(self, 'Open File', '', 'CSV(*.csv)', options=options)

        # If file is opened successfully, parse the data into the QTableView
        if InvGUI.filePath[0] != '':
            try:
                # parse the csv file
                with open(InvGUI.filePath[0], newline='') as csvFile:
                    self.tableWidget.setRowCount(0)
                    self.tableWidget.setColumnCount(2)
                    file = csv.reader(csvFile, delimiter=',', quotechar='|')

                    for rowData in file:
                        row = self.tableWidget.rowCount()
                        self.tableWidget.insertRow(row)

                        for column, colData in enumerate(rowData):
                            item = QTableWidgetItem(colData)
                            self.tableWidget.setItem(row, column, item)

                # Move to next page
                self.stackedWidget.setCurrentIndex(1)

            except:
                # If file is not loaded, display message
                warningMsg = QMessageBox()
                warningMsg.setIcon(QMessageBox.Warning)
                warningMsg.setWindowTitle('ERROR')
                warningMsg.setText('파일을 불러오지 못하였습니다.')
                warningMsg.exec_()

    # Displays data of the clicked row
    def ClickedCell(self, row, col):
        self.itemName.setText(self.tableWidget.item(row, 0).text())
        self.itemQuantity.setText(self.tableWidget.item(row, 1).text())
        InvGUI.row = row
        print("Row selected: ", InvGUI.row + 1)
        print("Column selected: ", col + 1)

    # Search and display corresponding content
    def Search(self):
        itemName = self.searchObj.text()
        print("Searching: ", itemName)

        # Searching for the item, with case insensitive format
        items = self.tableWidget.findItems(itemName, QtCore.Qt.MatchFixedString)
        if items:
            for item in items:
                InvGUI.row = item.row()
                # When found, display the results
                self.itemName.setText(self.tableWidget.item(InvGUI.row, 0).text())
                self.itemQuantity.setText(self.tableWidget.item(InvGUI.row, 1).text())
                self.tableWidget.selectRow(InvGUI.row)  # highlight corresponding row
                print("Row selected: ", InvGUI.row + 1)

        else:
            # When not found, display error message
            results = '존재하지 않는 품목입니다.'
            QMessageBox.information(self, 'Search Results', results)

    # Changes the quantity of the item selected
    def ChangeQuantity(self):
        # Prompt user with confirmation box before saving
        confirmSave = QMessageBox.question(self, 'Confirmation', "변경 사항을 저장 하시겠습니다?",
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        # If user clicks yes, apply changes and save file
        if confirmSave == QMessageBox.Yes:
            oldQty = int(self.tableWidget.item(InvGUI.row, 1).text())
            print("Old Quantity: ", oldQty)

            tmp = oldQty + int(self.incomingQuantity.text()) - int(self.outgoingQuantity.text())
            newQuantity = QTableWidgetItem(str(tmp))
            print("New Quantity: ", tmp)
            self.tableWidget.setItem(InvGUI.row, 1, newQuantity)
            InvGUI.SaveFile(self)  # call function to save file

    # Add new row with given item name and quantity and save its changes to the file
    def AddNewItem(self):
        print("adding")

    # Delete selected row and save its changes to the file
    def DeleteItem(self):
        print("deleting")

    # Save function that saves to the opened csv file of what current table widget contains
    def SaveFile(self):
        try:
            # Save to the same csv file by opening it again
            with open(InvGUI.filePath[0], newline='', mode='w') as csvFile:
                writer = csv.writer(csvFile)
                for row in range(self.tableWidget.rowCount()):
                    rowdata = []
                    for column in range(self.tableWidget.columnCount()):
                        item = self.tableWidget.item(row, column)
                        if item is not None:
                            rowdata.append(item.text())
                        else:
                            rowdata.append('')
                    writer.writerow(rowdata)

                # Display changes to the corresponding UI elements
                self.itemQuantity.setText(self.tableWidget.item(InvGUI.row, 1).text())

                # Set spin boxes to 0
                self.incomingQuantity.setValue(0)
                self.outgoingQuantity.setValue(0)

                # Inform user data was successfully saved
                confirmMsg = QMessageBox()
                confirmMsg.setIcon(QMessageBox.Information)
                confirmMsg.setWindowTitle('Confirmation')
                confirmMsg.setText("저장 되었습니다!")
                confirmMsg.exec_()

        except:
            # If file is not loaded, display message
            warningMsg = QMessageBox()
            warningMsg.setIcon(QMessageBox.Warning)
            warningMsg.setWindowTitle('ERROR')
            warningMsg.setText('오류가 발생하였습니다.')
            warningMsg.exec_()


app = QtWidgets.QApplication(sys.argv)
window = InvGUI()
window.show()
sys.exit(app.exec_())
