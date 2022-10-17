from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.uic import loadUi
from PyQt5.QtCore import QDir
import markdown
import pdfkit
import sys


class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()
        loadUi("main.ui", self)

        self.currentPath = None
        self.setWindowTitle("Nový")

        self.actionNewFile.triggered.connect(self.newFile)
        self.actionOpenFile.triggered.connect(self.openFile)
        self.actionSaveFile.triggered.connect(self.saveFile)
        self.actionSaveFileAs.triggered.connect(self.saveFileAs)
        self.actionUndo.triggered.connect(self.undo)
        self.actionRedo.triggered.connect(self.redo)
        self.actionCopy.triggered.connect(self.copy)
        self.actionPaste.triggered.connect(self.paste)
        self.actionCut.triggered.connect(self.cut)
        self.actionChangeFontSize14.triggered.connect(lambda: self.changeFontSize(14))
        self.actionChangeFontSize16.triggered.connect(lambda: self.changeFontSize(16))
        self.actionChangeFontSize18.triggered.connect(lambda: self.changeFontSize(18))
        self.actionChangeFontSize20.triggered.connect(lambda: self.changeFontSize(20))
        self.actionChangeFontSize22.triggered.connect(lambda: self.changeFontSize(22))
        self.actionChangeFontSize24.triggered.connect(lambda: self.changeFontSize(24))
        self.actionChangeFontSize28.triggered.connect(lambda: self.changeFontSize(28))
        self.actionChangeFontSize32.triggered.connect(lambda: self.changeFontSize(32))
        #self.actionClose.triggered.connect(exit)

    def newFile(self):
        self.textEdit.clear()
        self.setWindowTitle("Nový")
        self.currentPath = None
    
    def openFile(self):
        #options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        fname = QFileDialog.getOpenFileName(self, ("Otevřít soubor"), QDir().homePath(),  ("Text Files (*.txt *.md);; All Files(*.*)"), options=QFileDialog.DontUseNativeDialog)
        if fname[0] != "":
            with open(fname[0], "r") as f:
                self.textEdit.setText(f.read())
            self.setWindowTitle(fname[0])
            self.currentPath = fname[0]

    def saveFile(self):
        if self.currentPath != None:
            # save changes in current text file
            filetext = self.textEdit.toPlainText()
            with open(self.currentPath, "w") as f:
                f.write(filetext)
        else:
            self.saveFileAs()

    def saveFileAs(self):
        pathName = QFileDialog.getSaveFileName(self, "Uložit soubor", QDir().homePath(), ("Text Files (*.txt);; PDF (*.pdf)"), options=QFileDialog.DontUseNativeDialog)
        suffix = pathName[1][-5:-1]
        if pathName[0] != "":
            filetext = self.textEdit.toPlainText()
            with open(pathName[0] + suffix, "w") as f:
                f.write(filetext)
            self.setWindowTitle(pathName[0])
            self.currentPath = pathName[0]

    
    def undo(self):
        self.textEdit.undo()

    def redo(self):
        self.textEdit.redo()
        
    def copy(self):
        self.textEdit.copy()
        
    def paste(self):
        self.textEdit.paste()
    
    def cut(self):
        self.textEdit.cut()
    
    def changeFontSize(self, fontSize):
        self.textEdit.setFont(QFont("Arial", fontSize))

        

    def closeEvent(self, event):
        dialog = QMessageBox()
        dialog.setText("Chcete uložit soubor?")
        dialog.setWindowTitle("Textový editor")
        dialog.addButton(QPushButton("Ano"), QMessageBox.YesRole) #value - 0
        dialog.addButton(QPushButton("Ne"), QMessageBox.NoRole) #value - 1
        dialog.addButton(QPushButton("Zrušit"), QMessageBox.RejectRole) #value - 2

        answer = dialog.exec_()

        if answer == 0:
            self.saveFile()
            event.accept()
        elif answer == 2:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = Main()
    ui.show()
    app.exec_()