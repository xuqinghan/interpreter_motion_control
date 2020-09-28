# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction

from Ui_main import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.editor.setText("Hello\n")
        self.editor.append("world")
        self.editor.setLexer(None)
        self.editor.setUtf8(True)  # Set encoding to UTF-8

        action_new  = QAction(QIcon("./images/new.png"), "new", self)
        self.toolBar.addAction(action_new)
        action_new.triggered.connect(self.NewPlan)
        
        action_open  = QAction(QIcon("./images/open.png"), "open", self)
        self.toolBar.addAction(action_open)
        action_open.triggered.connect(self.OpenPlan)        
        
        action_save  = QAction(QIcon("./images/save.png"), "save", self)
        self.toolBar.addAction(action_save)
        action_save.triggered.connect(self.SavePlan)    
        
        action_reset  = QAction(QIcon("./images/reset.png"), "reset", self)
        self.toolBar.addAction(action_reset)
        action_reset.triggered.connect(self.ResetPlan)   
        
        action_play  = QAction(QIcon("./images/play.png"), "play", self)
        self.toolBar.addAction(action_play)
        action_play.triggered.connect(self.PlayPlan)
        
        action_step  = QAction(QIcon("./images/step.png"), "step", self)
        self.toolBar.addAction(action_step)
        action_step.triggered.connect(self.StepPlan)        
        
        action_stop  = QAction(QIcon("./images/stop.png"), "stop", self)
        self.toolBar.addAction(action_stop)
        action_stop.triggered.connect(self.StopPlan)   
        
        action_pause  = QAction(QIcon("./images/pause.png"), "pause", self)
        self.toolBar.addAction(action_pause)
        action_pause.triggered.connect(self.PausePlan)   
        
    def NewPlan(self, b):
        print("pressed new ")
        #self.text.setText(a.text())
        
    def OpenPlan(self, b):
        print("pressed open ")
        
    def SavePlan(self, b):
        print("pressed save ")   
        
    def ResetPlan(self, b):
        print("pressed reset ")    
        
    def PlayPlan(self, b):
        print("pressed play ")    
        
    def StepPlan(self, b):
        print("pressed step ")            
        
    def StopPlan(self, b):
        print("pressed step ") 
        
    def PausePlan(self,  b):
        print("pressed pause ")         
