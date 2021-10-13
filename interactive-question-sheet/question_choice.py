from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QLabel, QWidget
from toggle_type import ToggleType

class QuestionChoice(QLabel):
    
    def __init__(self, sequence: str, text: str):
        QWidget.__init__(self)
        self.sequence = sequence
        self.setText(f'({sequence}) {text}')
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        self.is_selected = False
        self.is_hint = False
        
    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.toggle(ToggleType.SELECT)

        return super().mousePressEvent(ev)

    """
    @property
    def is_selected(self):
        return self.__is_selected
    
    @is_selected.setter
    def is_selected(self, is_selected):
        self.__is_selected = is_selected
    """
    def set_bg_color(self):
        color = ''
        if self.is_selected and self.is_hint:
            color = '#cccccc'
        elif self.is_selected:
            color = '#cccccc'
        elif self.is_hint:
            color = '#edffb5'
        else:
            color = 'transparent'
        self.setStyleSheet(f'background-color: {color}')

    def toggle(self, toggle_type):
        
        if toggle_type == ToggleType.SELECT:
            if self.parent().selected_seq != self.sequence and \
            self.parent().selected_seq != '':
                return

            self.is_selected = not self.is_selected

            if self.is_selected:
                self.parent().selected_seq = self.sequence
            else:
                self.parent().selected_seq = ''
        elif toggle_type == ToggleType.HINT:
            self.is_hint = not self.is_hint
        
        self.set_bg_color()
        

    '''
    def toggle_selected(self):
        

        self.is_selected = not self.is_selected

        if self.is_selected:
            self.parent().selected_seq = self.sequence
            #self.setStyleSheet('background-color: #cccccc;')
        else:
            self.parent().selected_seq = ''
            #self.setStyleSheet('background-color: transparent;')    

        self.setStyleSheet(f'background-color: {self.get_bg_color()}')
    '''


