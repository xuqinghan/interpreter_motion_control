import sys
from PyQt5.QtWidgets import QApplication,QMainWindow
#import test     # module test.py
from main import MainWindow 
 
 
if __name__ == '__main__':
    app = QApplication(sys.argv)
    myMainWindow = MainWindow()
    #myUi = test.Ui_MainWindow()
    #myUi.setupUi(myMainWindow)
    myMainWindow.show()
    sys.exit(app.exec_())
