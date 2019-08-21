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

    # Opens a single .csv file
    def OpenFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filePath = QFileDialog.getOpenFileName(self, 'Open File', '', 'CSV(*.csv)', options=options)

        # If file is opened successfully, parse the data into the QTableView
        if filePath[0] != '':
            try:
                # parse the csv file
                with open(filePath[0], newline='') as csvFile:
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
                warningMsg.setText('Error loading file')
                warningMsg.exec_()

    # Displays data of the clicked row
    def ClickedCell(self, row, col):
        print("Selected cell is: ", row, col)
        self.itemName.setText(self.tableWidget.item(row, 0).text())
        self.itemQuantity.setText(self.tableWidget.item(row, 1).text())

    # Search and display corresponding content
    def Search(self):
        itemName = self.searchObj.text()
        print("Searching: ", itemName)

        # Searching for the item, with case insensitive format
        items = self.tableWidget.findItems(itemName, QtCore.Qt.MatchFixedString)
        if items:
            for item in items:
                row = item.row()
                # When found, display the results
                self.itemName.setText(self.tableWidget.item(row, 0).text())
                self.itemQuantity.setText(self.tableWidget.item(row, 1).text())
                self.tableWidget.selectRow(row)

        else:
            # When not found, display error message
            results = '존재하지 않는 품목입니다.'
            QMessageBox.information(self, 'Search Results', results)


app = QtWidgets.QApplication(sys.argv)
window = InvGUI()
window.show()
sys.exit(app.exec_())