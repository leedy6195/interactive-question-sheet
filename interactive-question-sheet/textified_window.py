import re
import time
import csv
from PyQt5 import QtCore
from PyQt5.QtCore import QTimer, Qt, QSize
from PyQt5.QtWidgets import QCheckBox, QHBoxLayout, QLCDNumber, QLabel, QScrollArea, QWidget, \
    QPushButton, QVBoxLayout
from modules import pdf_miner
from toggle_type import ToggleType
from question_box import QuestionBox
from question_choice import QuestionChoice

class TextifiedWindow(QWidget):
    switch_window = QtCore.pyqtSignal()
    qboxes = []

    def __init__(self, question_path, answer_path, remaining_second):
        
        QWidget.__init__(self)
        self.question_path = question_path
        self.answer_path = answer_path
        self.remaining_second = remaining_second
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('interactive question sheet')
        self.setFixedSize(QSize(400, 400))
        vbox = QVBoxLayout()
        scroll = QScrollArea()
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll.setWidgetResizable(True)
        widget_scroll = QWidget()
        vbox_scroll = QVBoxLayout()
        widget_scroll.setLayout(vbox_scroll)

        txt = pdf_miner.pdf_to_text(self.question_path)
        
        pattern = '(\d+)[.]\s([A-Z](?:.*\n)*?)((?:\([A-D]\)\s.*\n){4})'
        pattern2 = '\(([A-D])\)\s((?:(?!\\\).)*)'

        for m in re.finditer(pattern ,txt):
            choices = []

            for m2 in re.finditer(pattern2, m.group(3)):
                choices.append(QuestionChoice(m2.group(1), m2.group(2)))

            widget = QuestionBox(int(m.group(1)), m.group(2).replace('\n\n','\n'), choices)
            
            self.qboxes.append(widget)
            vbox_scroll.addWidget(widget)
        
        scroll.setWidget(widget_scroll)
        vbox.addWidget(scroll)

        print(len(list(filter(lambda q : q.number % 2 == 0, self.qboxes))))

        hbox = QHBoxLayout()
        

        self.lcd = QLCDNumber()
        self.lcd.setDigitCount(8)
        self.lcd.setSegmentStyle(QLCDNumber.SegmentStyle.Flat)
        self.lcd.setStyleSheet('border: 0px;')
        
        self.timer = QTimer(self)
        self.timer.start(1000)
        self.lcd.display(time.strftime('%H:%M:%S', time.gmtime(self.remaining_second)))
        self.timer.timeout.connect(lambda:self.run())

        self.checkbox = QCheckBox()
        self.result = QLabel()
        self.result.setFixedWidth(100)
        button = QPushButton("submit")
        button.setFixedWidth(100)

        hbox.addWidget(self.lcd)
        hbox.addStretch()
        hbox.addWidget(self.checkbox)
        hbox.addWidget(QLabel("show hint"))
        hbox.addStretch()
        hbox.addWidget(self.result)
        hbox.addStretch()
        hbox.addWidget(button)

        vbox.addLayout(hbox)
        self.setLayout(vbox)

        button.clicked.connect(self.submit)
        self.checkbox.clicked.connect(self.toggle_hint)
        ###
        f = open(self.answer_path)
        reader = csv.reader(f)
        self.answers = list(reader)
        del self.answers[0]
        f.close()

        
        
    def toggle_hint(self):
        for row in self.answers:
            q = next((x for x in self.qboxes if str(x.number) == row[0]), None)
            c = next((x for x in q.choices if x.sequence == row[1]), None)
            c.toggle(ToggleType.HINT)

    def submit(self):
        answerset = set()
        for qbox in self.qboxes:
            answerset.add((str(qbox.number), qbox.selected_seq))
        
        count = 0
        for row in self.answers:
            if tuple(row) in answerset:
                count += 1
        
        self.result.setText(f'{count} / {len(self.qboxes)}')

    def run(self):
        self.remaining_second = self.remaining_second - 1
        self.lcd.display(time.strftime('%H:%M:%S', time.gmtime(self.remaining_second)))
        if self.remaining_second == 0:
            self.timer.stop()