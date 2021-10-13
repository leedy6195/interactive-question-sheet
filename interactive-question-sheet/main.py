import sys
from PyQt5.QtWidgets import QApplication

from main_window import MainWindow
from textified_window import TextifiedWindow

class Controller:
    
    def __init__(self):
        pass

    def show_main(self):
        self.main = MainWindow()
        self.main.switch_window.connect(self.show_textified)
        self.main.show()

    def show_textified(self, question_path, answer_path, remaining_second):
        self.textified = TextifiedWindow(question_path, answer_path, remaining_second)
        self.textified.switch_window.connect(self.show_main)
        self.main.close()
        self.textified.show()

def main():
    app = QApplication(sys.argv)
    controller = Controller()
    controller.show_main()
    
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

