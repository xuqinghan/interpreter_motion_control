from PyQt5 import Qsci
from PyQt5.QtGui import QIcon,  QColor, QFont

class CustomLexer(Qsci.QsciLexerCustom):

    def __init__(self, parent): 
        Qsci.QsciLexerCustom.__init__(self,  parent) 
        self._styles = { 
         0: 'Default', 
         1: 'Comment', 
         2: 'Key', 
         3: 'Assignment', 
         4: 'Value', 
        }
        for key,value in self._styles.items(): 
            setattr(self, value, key) 

    def description(self, style): 
        return self._styles.get(style, '') 

    def defaultColor(self, style): 
        if style == self.Default: 
            return QColor('#000000') 
        elif style == self.Comment: 
            return QColor(255,  0,  0) 
        elif style == self.Key: 
            return QColor('#0000CC') 
        elif style == self.Assignment: 
            return QColor('#CC0000') 
        elif style == self.Value: 
            return QColor('#00CC00') 
        return Qsci.QsciLexerCustom.defaultColor(self, style) 

    def styleText(self, start, end): 
        editor = self.editor() 
        if editor is None: 
            return

        # scintilla works with encoded bytes, not decoded characters. 
        # this matters if the source contains non-ascii characters and 
        # a multi-byte encoding is used (e.g. utf-8) 
        source = '' 
        if end > editor.length(): 
            end = editor.length() 
        if end > start: 
            # if sys.hexversion >= 0x02060000: 
                # faster when styling big files, but needs python 2.6 
                source = bytearray(end - start) 
                editor.SendScintilla(editor.SCI_GETTEXTRANGE, start, end, source)
            # else: 
            #     source = unicode(editor.text() 
            #                     ).encode('utf-8')[start:end] 
        if not source: 
            return 

        # the line index will also be needed to implement folding 
        index = editor.SendScintilla(editor.SCI_LINEFROMPOSITION, start) 
        if index > 0: 
            # the previous state may be needed for multi-line styling 
            pos = editor.SendScintilla(editor.SCI_GETLINEENDPOSITION, index - 1) 
            state = editor.SendScintilla(editor.SCI_GETSTYLEAT, pos) 
        else: 
            state = self.Default

        self.startStyling(start, 0x1f) 

        # scintilla always asks to style whole lines 
        for line in source.splitlines(True): 
            length = len(line) 
            if line.startswith(b'#'): 
                state = self.Comment 
            else: 
                # the following will style lines like "x = 0" 
                pos = line.find(b'=') 
                if pos > 0: 
                    self.setStyling(pos, self.Key) 
                    self.setStyling(1, self.Assignment) 
                    length = length - pos - 1 
                    state = self.Value 
                else: 
                    state = self.Default 
            self.setStyling(length, state) 
            # folding implementation goes here 
            index += 1 
