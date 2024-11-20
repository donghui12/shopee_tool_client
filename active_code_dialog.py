from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt

class ActiveCodeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("激活码验证")
        self.setFixedSize(300, 150)
        
        layout = QVBoxLayout()
        
        # 提示文本
        label = QLabel("请输入激活码:")
        label.setStyleSheet("font-size: 14px; margin-bottom: 10px;")
        
        # 激活码输入框
        self.active_code_input = QLineEdit()
        self.active_code_input.setPlaceholderText("请输入激活码")
        self.active_code_input.setMinimumHeight(35)
        self.active_code_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #4CAF50;
            }
        """)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        
        # 确定按钮
        confirm_button = QPushButton("确定")
        confirm_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                min-width: 80px;
                min-height: 35px;
            }
            QPushButton:hover { background-color: #45a049; }
        """)
        confirm_button.clicked.connect(self.accept)
        
        # 取消按钮
        cancel_button = QPushButton("取消")
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                min-width: 80px;
                min-height: 35px;
            }
            QPushButton:hover { background-color: #da190b; }
        """)
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(confirm_button)
        button_layout.addWidget(cancel_button)
        
        layout.addWidget(label)
        layout.addWidget(self.active_code_input)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def get_active_code(self):
        return self.active_code_input.text() 