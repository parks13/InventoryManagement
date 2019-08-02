import sys, csv
from PyQt5 import QtCore, uic, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QTextEdit, \
    QVBoxLayout, QWidget, QFileDialog, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QTextCharFormat, QTextFormat, QTextObjectInterface
from PyQt5.QtCore import QFile, QIODevice, QObject, QSizeF

# Load the UI file
UIClass, QtBaseClass = uic.loadUiType(".files\\InvScreen.ui")

# Class to handle the GUI of the program
class InvGUI(UIClass, QtBaseClass):
    # Constructs the GUI
    def __init__(self):
        UIClass.__init__(self)
        QtBaseClass.__init__(self)
        self.setupUi(self)
        self.setWindowTitle('Inventory Management Program')  # set the title of the program window
        self.setWindowFlag(QtCore.Qt.WindowMinMaxButtonsHint, False)  # disable windows maximize button
#       self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)  # disable windows exit button

        # Show open file page and let the user open csv file and proceed to next page
        self.stackedWidget.setCurrentIndex(0)
        self.openFileButton.clicked.connect(self.OpenFile)

        # Connect cellClicked event to a function displaying its related values
        self.tableWidget.cellClicked.connect(self.ClickedCell)

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
    def ClickedCell(self, row, column):
        tmp = self.tableWidget.itemAt(row, column)

        # if tmp != '':
        #     # Check if selected value is item name or item quantity
        #     if not tmp.isnumeric():
        #         self.itemName.setText(tmp.text())
        #         tmp = self.tableWidget.itemAt(row, column+1)
        #         self.itemQuantity.setText(tmp.text())
        # 
        #     else:
        #         self.itemQuantity.setText(tmp.text())
        #         tmp = self.tableWidget.itemAt(row, column - 1)
        #         self.itemName.setText(tmp.text())


app = QtWidgets.QApplication(sys.argv)
window = InvGUI()
window.show()
sys.exit(app.exec_())