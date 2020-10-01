# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon,  QColor, QFont
from PyQt5.QtWidgets import QAction, QFileDialog
from lexer import CustomLexer
from PyQt5.Qsci import QsciScintilla

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


        self.editor.setUtf8(True)  # Set encoding to UTF-8
        #行号显示区域
        #self.editor.setMarginType(0, QsciScintilla::NumberMargin)
        self.editor.setMarginLineNumbers(0, True)
        self.editor.setMarginWidth(0, 30)

        self.editor.setColor(QColor(255, 255, 255))          #设置默认的字体颜色
        self.editor.setPaper(QColor(0, 0, 0))    #设置底色
        
        font_normal = QFont("monospace", 14, QFont.Bold)
        self.editor.setFont(font_normal)    #默认的字体加粗。
        sdcc_kwlist = ['BEG',  'END',  'DEFINE',  'BODY',  'WAIT',  'CAMERA',  'MOVE', 'STOP',  'RESET ALL',  '↑',  '↓',  '←',  '→']
        self.editor.SendScintilla(QsciScintilla.SCI_SETKEYWORDS, 0," ".join(sdcc_kwlist).encode(encoding='utf-8'))

#        self.lexer = CustomLexer(self.editor)
#        self.editor.setLexer(self.lexer) #QsciScintilla



        action_new  = QAction(QIcon("./images/new.png"), "new", self)
        self.toolBar.addAction(action_new)
        action_new.triggered.connect(self.NewPlan)
        
        action_open  = QAction(QIcon("./images/open.png"), "open", self)
        self.toolBar.addAction(action_open)
        action_open.triggered.connect(self.OpenPlan)        
        
        action_save  = QAction(QIcon("./images/save.png"), "save", self)
        self.toolBar.addAction(action_save)
        action_save.triggered.connect(self.SavePlan)    
        
        action_reset  = QAction(QIcon("./images/reset.png"), "复位", self)
        self.toolBar.addAction(action_reset)
        action_reset.triggered.connect(self.ResetPlan)   
        
        action_play  = QAction(QIcon("./images/play.png"), "运行", self)
        self.toolBar.addAction(action_play)
        action_play.triggered.connect(self.PlayPlan)
        
        action_step  = QAction(QIcon("./images/step.png"), "单步", self)
        self.toolBar.addAction(action_step)
        action_step.triggered.connect(self.StepPlan)
        
        action_stop  = QAction(QIcon("./images/stop.png"), "停止", self)
        self.toolBar.addAction(action_stop)
        action_stop.triggered.connect(self.StopPlan)   
        
        action_pause  = QAction(QIcon("./images/pause.png"), "暂停", self)
        self.toolBar.addAction(action_pause)
        action_pause.triggered.connect(self.PausePlan)   
        
    def NewPlan(self, b):
        print("pressed new ")
        #self.text.setText(a.text())
        
    def OpenPlan(self, b):
        print("pressed open ")
        #    def openfile(self):
        openfile_name,  *_ = QFileDialog.getOpenFileName(self,'选择计划','./plans','Plan files(*.pln)')
        print(openfile_name)
        self.editor.setText("") 
        with open(openfile_name,  'r',  encoding='utf-8') as f:
            for line in f.readlines():
                #self.editor.setText("Hello\n")
                self.editor.append(line)
        
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
