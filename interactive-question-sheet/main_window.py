from PyQt5 import QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QMessageBox, QWidget, \
    QPushButton, QVBoxLayout, QFileDialog

class MainWindow(QWidget):
    
    switch_window = QtCore.pyqtSignal(str, str, int)

    def __init__(self):
        QWidget.__init__(self)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('interactive question sheet')
        self.setFixedSize(QSize(600, 160))
        
        vbox_main = QVBoxLayout()

        #question hbox
        hbox_question = QHBoxLayout()
        
        self.label_question = QLabel("", self)
        self.label_question.setFixedWidth(300)
        self.label_question.setWordWrap(True)
        self.button_question = QPushButton('select')
        self.button_question.setFixedWidth(100)
        
        hbox_question.addWidget(QLabel('question sheet (PDF)'))
        hbox_question.addWidget(self.label_question)
        hbox_question.addWidget(self.button_question)
        
        #answer hbox
        hbox_answer = QHBoxLayout()

        self.label_answer = QLabel("", self)
        self.label_answer.setFixedWidth(300)
        self.label_answer.setWordWrap(True)
        self.button_answer = QPushButton('select')
        self.button_answer.setFixedWidth(100)

        hbox_answer.addWidget(QLabel('answer sheet (CSV)'))
        hbox_answer.addWidget(self.label_answer)
        hbox_answer.addWidget(self.button_answer)

        #time limit hbox
        hbox_time = QHBoxLayout()

        self.label_time = QLabel('time limit (min)')
        self.label_time.setFixedWidth(165)
        self.le_time = QLineEdit()
        self.le_time.setFixedWidth(35)
        self.le_time.setMaxLength(3)

        hbox_time.addWidget(self.label_time)
        hbox_time.addWidget(self.le_time)
        hbox_time.addStretch()

        #bottom hbox
        hbox_bottom = QHBoxLayout()
        self.button_submit = QPushButton("textify")
        self.button_submit.setFixedWidth(100)

        hbox_bottom.addStretch(1)
        hbox_bottom.addWidget(self.button_submit)
        hbox_bottom.addStretch(1)

        #set up vbox
        vbox_main.addLayout(hbox_question)
        vbox_main.addLayout(hbox_answer)
        vbox_main.addLayout(hbox_time)
        vbox_main.addStretch()
        vbox_main.addLayout(hbox_bottom)
        
        self.setLayout(vbox_main)

        self.button_question.clicked.connect(self.open_question)
        self.button_answer.clicked.connect(self.open_answer)
        self.button_submit.clicked.connect(self.textify)

   
    def open_question(self):
        path = QFileDialog.getOpenFileName(self, 'Choose question file.', '',
                                        'PDF file(*.pdf)')
        if path != ('', ''):       
            self.label_question.setText(path[0])

    def open_answer(self):
        path = QFileDialog.getOpenFileName(self, 'Choose answer file.', '',
                                        'CSV file(*.csv)')
        if path != ('', ''):       
            self.label_answer.setText(path[0])        
    def textify(self):
        if self.label_question.text() == '':
            QMessageBox.warning(self, '', 'please select a question sheet.')
            return
        if self.label_answer.text() == '':
            QMessageBox.warning(self, '', 'please select an answer sheet.')
            return
        if not self.le_time.text().isdecimal() or self.le_time.text() == '':
            QMessageBox.warning(self, '', 'please enter the time limit .')
            return

        self.switch_window.emit(
            self.label_question.text(), self.label_answer.text(), int(self.le_time.text()) * 60
            )
