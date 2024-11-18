import sys
from PyQt6.QtWidgets import QApplication
from login import LoginWindow
from main_window import MainWindow

class ShopeeTools:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.login_window = LoginWindow()
        self.main_window = None
        
    def show_main_window(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.login_window.close()
        
    def run(self):
        self.login_window.show()
        return self.app.exec()

if __name__ == '__main__':
    app = ShopeeTools()
    sys.exit(app.run())