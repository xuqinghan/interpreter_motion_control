# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt5.QtCore import pyqtSlot,  pyqtSignal,  QThread
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon,  QColor, QFont
from PyQt5.QtWidgets import QAction, QFileDialog
from lexer import CustomLexer
from PyQt5.Qsci import QsciScintilla

from Ui_main import Ui_MainWindow

from interpreter import compile_time
import u_comm
import time

class WorkerPlan(QThread):
    move_to_line = pyqtSignal(int)

    def __init__(self, parent=None):
        super(WorkerPlan, self).__init__(parent)
        #设置工作状态与初始num数值
        self.working = False
        self.current_ptr = 0
        #LABEL对应的指针
        self.LABEL_prt_dict = {}
        self.CMDS_LINES = []
    
    def reset(self):
        '''不改变程序，只是恢复到重头开始执行位置'''
        self.numline = 0

    def load(self,  lines_plan):
        '''打开新文本'''
        self.reset()
        lines_plan = [line.strip(' \n') for line in lines_plan ]
        #print(lines_plan)
        self.CMDS_LINES = compile_time(lines_plan)
        self.LABEL_prt_dict = {}
        self.current_ptr = 0

#    def __del__(self):
#        #线程状态改变与线程终止
#        self.working = False
#        self.wait()

    def step(self):
        '''一次执行1行 光标移到下一行'''
        # 发射信号
        num_line1, CMD_LINE1 = self.CMDS_LINES[self.current_ptr]
        #改成编辑器界面中从1开始的行号
        num_line1 += 1
        print(f'执行第{num_line1}行')
        if self.current_ptr < len(self.CMDS_LINES):
            #单步确认，继续执行
            if isinstance(CMD_LINE1, list):
                #如果是多行 只移动1次行号
                for IL_line1 in CMD_LINE1:
                    self.run_IL_line1(IL_line1)
                self.current_ptr  += 1
            elif isinstance(CMD_LINE1, tuple):
                #单行 goto特殊处理 行号
                print(CMD_LINE1)
                num_line1_goto = self.run_IL_line1(CMD_LINE1)

                if num_line1_goto is not None:
                    #goto语句 光标跳转了，current_ptr在goto里改变了，不需要+1
                    num_line1 = num_line1_goto
                else:
                    #没有goto 光标前进1
                    self.current_ptr  += 1

            self.move_to_line.emit(num_line1)

        else:
            print('执行完毕')

    def run(self):
        self.working = True
        while self.current_ptr < len(self.CMDS_LINES):
            if self.working:
                self.step()
            else:
                break
        print('执行完毕')

    def run_IL_line1(self, IL_line1):
        '''执行1行plan语句
            goto 返回行号
        '''
        CMD, *para = IL_line1
        num_line1_goto = None
        if CMD == 'GOTO':
            #参数是label 
            self.current_ptr = self.LABEL_prt_dict[para[0]]
            print(f'GOTO {self.CMDS_LINES[self.current_ptr]}')
            num_line1_goto, CMD_LINE1 = self.CMDS_LINES[self.current_ptr]
        else:
            if CMD == 'LABEL':
                #参数是label
                self.LABEL_prt_dict[para[0]] = self.current_ptr
                print('LABEL')
            elif CMD == 'MOVE':
                u_comm.send1(para[0])
            elif CMD == 'WAIT':
                print(f'等待 {para[0]} 秒')
                time.sleep(para[0])
                #用qt线程的定时，不用time
                #self.sleep(int(para[0]))
            else:
                raise Exception(f"invalid IL {CMD}")
        return num_line1_goto



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

        self.editor.setCaretLineBackgroundColor(QColor(0, 0, 255));
        #self.editor.setReadOnly(True)

        
        font_normal = QFont("monospace", 14, QFont.Bold)
        self.editor.setFont(font_normal)    #默认的字体加粗。
        sdcc_kwlist = ['BEG',  'END',  'DEFINE',  'BODY',  'WAIT',  'CAMERA',  'MOVE', 'STOP',  'RESET ALL',  '↑',  '↓',  '←',  '→']
        self.editor.SendScintilla(QsciScintilla.SCI_SETKEYWORDS, 0," ".join(sdcc_kwlist).encode(encoding='utf-8'))

#        self.lexer = CustomLexer(self.editor)
#        self.editor.setLexer(self.lexer) #QsciScintilla



        self.action_new  = QAction(QIcon("./images/new.png"), "new", self)
        self.toolBar.addAction(self.action_new)
        self.action_new.triggered.connect(self.NewPlan)
        
        self.action_open  = QAction(QIcon("./images/open.png"), "open", self)
        self.toolBar.addAction(self.action_open)
        self.action_open.triggered.connect(self.OpenPlan)        
        
        self.action_save  = QAction(QIcon("./images/save.png"), "save", self)
        self.toolBar.addAction(self.action_save)
        self.action_save.triggered.connect(self.SavePlan)    
        self.action_save.setEnabled(False)
        
        self.action_reset  = QAction(QIcon("./images/reset.png"), "复位", self)
        self.toolBar.addAction(self.action_reset)
        self.action_reset.triggered.connect(self.ResetPlan)   
        self.action_reset.setEnabled(False)
        
        self.action_play  = QAction(QIcon("./images/play.png"), "运行", self)
        self.toolBar.addAction(self.action_play)
        self.action_play.triggered.connect(self.PlayPlan)
        self.action_play.setEnabled(False)
        
        self.action_step  = QAction(QIcon("./images/step.png"), "单步", self)
        self.toolBar.addAction(self.action_step)
        self.action_step.triggered.connect(self.StepPlan)
        self.action_step.setEnabled(False)
        
#        self.action_stop  = QAction(QIcon("./images/stop.png"), "停止", self)
#        self.toolBar.addAction(self.action_stop)
#        self.action_stop.triggered.connect(self.StopPlan)   
#        self.action_stop.setEnabled(False)
        
        self.action_pause  = QAction(QIcon("./images/pause.png"), "暂停", self)
        self.toolBar.addAction(self.action_pause)
        self.action_pause.triggered.connect(self.PausePlan)   
        self.action_pause.setEnabled(False)
        
        
        self.thread_worker = WorkerPlan()
        self.thread_worker.move_to_line.connect(self.set_cursor_numline)
        
    def set_cursor_numline(self, num_line):
        self.editor.setCursorPosition(num_line,0)
        self.editor.SendScintilla(QsciScintilla.SCI_SETFIRSTVISIBLELINE, num_line+1);



    def set_Plan_editing(self):
        '''计划文件处于可编辑模式'''
        self.editor.setCaretLineVisible(True)
        self.editor.setCaretLineBackgroundColor(QColor(0, 255, 0));
        self.editor.setReadOnly(False) #可编辑
        self.editor.setMouseTracking(True) #可改变光标位置
        #可运行
        self.action_play.setEnabled(True)
        self.action_step.setEnabled(True)
        self.action_new.setEnabled(True)
        self.action_open.setEnabled(True)
        
        
    def set_Plan_runtime(self,  is_step=True):
        '''计划文件处于运行中模式'''
        self.editor.setCaretLineBackgroundColor(QColor(0, 0, 255));
        self.editor.setMouseTracking(False) #不可改变光标位置
        self.editor.setReadOnly(True) #b不可编辑
        self.action_pause.setEnabled(True) #可暂停

        #运行中不可新建，不可打开别的
        self.action_new.setEnabled(False)
        self.action_open.setEnabled(False)
        

#    def set_Plan_stop(self):
#        '''停止运行，可以新建，打开'''
#        self.action_new.setEnabled(True)
#        self.action_open.setEnabled(True)
    
    
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
            lines_plan = f.readlines()

        #加载到编辑器显示
        for line in lines_plan:
                #self.editor.setText("Hello\n")
                self.editor.append(line)
        
        #加载到执行器
        self.thread_worker.load(lines_plan)

        num_line = 0
        self.set_cursor_numline(num_line)
        self.set_Plan_editing()
        
    def SavePlan(self, b):
        print("pressed save ")   
        
    def ResetPlan(self, b):
        print("pressed reset ")    
        #复位 恢复编辑
        self.reset()
        self.set_Plan_editing()
        
    def PlayPlan(self, b):
        print("pressed play ")    
        self.set_Plan_runtime()
        self.action_reset.setEnabled(False) #可复位
        self.action_pause.setEnabled(True) #自动模式需要暂停
        self.thread_worker.start()
        
        
    def StepPlan(self, b):
        print("pressed step ")
        self.set_Plan_runtime()
        self.action_reset.setEnabled(True) #可复位
        self.action_pause.setEnabled(False) #单步不需要暂停
        self.thread_worker.step()
        
    def StopPlan(self, b):
        print("pressed step ") 
        
    def PausePlan(self,  b):
        print("pressed pause ")         
        self.thread_worker.working = False
        self.action_reset.setEnabled(True) #可复位
