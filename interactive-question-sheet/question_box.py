from PyQt5.QtWidgets import QVBoxLayout, QWidget
from question_choice import QuestionChoice
from PyQt5.QtWidgets import QLabel

class QuestionBox(QWidget):

    def __init__(self, number: int, title: str, choices: list[QuestionChoice]):
        QWidget.__init__(self)
        self.number = number
        self.title = title
        self.choices = choices
        self.init_ui()
        self.selected_seq = ''

    def init_ui(self):
        vbox = QVBoxLayout()
        self.setLayout(vbox)
    
        title = QLabel(f'{str(self.number)}. {self.title}')
        title.setWordWrap(True)
        vbox.addWidget(title)

        
        for choice in self.choices:
            vbox.addWidget(choice)

