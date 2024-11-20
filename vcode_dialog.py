from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, 
                           QLineEdit, QPushButton, QHBoxLayout)
from PyQt6.QtCore import Qt

class VCodeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("验证码")
        self.setFixedSize(300, 150)
        
        # 创建布局
        layout = QVBoxLayout()
        
        # 提示文本
        label = QLabel("请输入验证码:")
        label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                margin-bottom: 10px;
            }
        """)
        
        # 验证码输入框
        self.vcode_input = QLineEdit()
        self.vcode_input.setPlaceholderText("请输入验证码")
        self.vcode_input.setMinimumHeight(35)
        self.vcode_input.setStyleSheet("""
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
        confirm_button.setMinimumHeight(35)
        confirm_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        confirm_button.clicked.connect(self.accept)
        
        # 取消按钮
        cancel_button = QPushButton("取消")
        cancel_button.setMinimumHeight(35)
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
            QPushButton:pressed {
                background-color: #d32f2f;
            }
        """)
        cancel_button.clicked.connect(self.reject)
        
        # 添加按钮到按钮布局
        button_layout.addWidget(confirm_button)
        button_layout.addWidget(cancel_button)
        
        # 添加所有组件到主布局
        layout.addWidget(label)
        layout.addWidget(self.vcode_input)
        layout.addLayout(button_layout)
        
        # 设置主布局
        self.setLayout(layout)
        
    def get_vcode(self):
        """获取输入的验证码"""
        return self.vcode_input.text() 