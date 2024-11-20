import sys
from PyQt6.QtWidgets import QApplication
from login import LoginWindow
from main_window import MainWindow

class ShopeeTools:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.login_window = None
        self.main_window = None
        
    def show_login(self):
        self.login_window = LoginWindow(self)
        self.login_window.show()
        
    def show_main_window(self, username):
        self.main_window = MainWindow(username)
        self.main_window.show()
        if self.login_window:
            self.login_window.close()
        
    def run(self):
        self.show_login()
        return self.app.exec()

if __name__ == '__main__':
    app = ShopeeTools()
    sys.exit(app.run())