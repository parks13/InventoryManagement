import sys, csv
from PyQt5 import QtCore, uic, QtWidgets, QtGui
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QLineEdit, QMessageBox, QPushButton, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtGui import QTextCharFormat, QTextFormat, QTextObjectInterface
from PyQt5.QtCore import QFile, QIODevice, QObject, QSizeF

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
#       self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)  # disable windows exit button

        # Show open file page and let the user open csv file and proceed to next page
        self.stackedWidget.setCurrentIndex(0)
        self.openFileButton.clicked.connect(self.openFile)


    # Opens a single .csv file
    def openFile(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        filePath = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File', '*.csv', options=options)
        file = QFile(filePath)

        # If file is opened successfully, parse the data into the QTableView
        if file:

            # parse the csv file
            with open(file, "w") as fileInput:
                for row in csv.reader(fileInput):
                    items = [
                        QtGui.QStandardItem(field)
                        for field in row
                    ]
                    self.tableView.appendRow(items)

            # Move to next page
            self.stackedWidget.setCurrentIndex(1)

        # If file is not open, display message and stay on same page
        else:
            QMessageBox.warning(self, "ERROR", '','','')


app = QtWidgets.QApplication(sys.argv)
window = InvGUI()
window.show()
sys.exit(app.exec_())