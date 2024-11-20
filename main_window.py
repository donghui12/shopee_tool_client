from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QLabel, QFrame, QLineEdit, QMessageBox)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QFont
import requests

class MainWindow(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.api_base_url = "http://localhost:8080/v1/shopee"
        self.setup_ui()
        
    def setup_ui(self):
        # 设置窗口基本属性
        self.setWindowTitle('ShopeeTools')
        self.resize(900, 600)
        
        # 创建中央窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # 左侧菜单
        left_menu = self.create_left_menu()
        
        # 右侧内容区
        right_content = self.create_right_content()
        
        main_layout.addWidget(left_menu)
        main_layout.addWidget(right_content, 1)  # 1表示拉伸因子
        
    def create_left_menu(self):
        left_menu = QFrame()
        left_menu.setFixedWidth(200)
        left_menu.setStyleSheet("background-color: #2C2C2C;")
        
        layout = QVBoxLayout(left_menu)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # 添加菜单按钮
        menu_buttons = ['出货时间设置', '其他功能']
        for text in menu_buttons:
            btn = QPushButton(text)
            btn.setFixedHeight(50)
            btn.setFont(QFont("Arial", 12))
            btn.setStyleSheet("""
                QPushButton {
                    color: white;
                    border: none;
                    text-align: left;
                    padding-left: 20px;
                }
                QPushButton:hover { background-color: #3C3C3C; }
            """)
            layout.addWidget(btn)
        
        layout.addStretch()
        return left_menu
        
    def create_right_content(self):
        right_content = QFrame()
        right_content.setStyleSheet("background-color: #F5F5F5;")
        
        layout = QVBoxLayout(right_content)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 标题
        title = QLabel("出货时间设置")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        
        # 时间输入框
        time_layout = QHBoxLayout()
        time_label = QLabel("出货时间:")
        self.time_input = QLineEdit()
        self.time_input.setPlaceholderText("请输入出货时间")
        self.time_input.setMinimumHeight(35)
        self.time_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 14px;
            }
            QLineEdit:focus { border: 1px solid #4CAF50; }
        """)
        
        update_button = QPushButton("更新")
        update_button.setFixedWidth(100)
        update_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                min-height: 35px;
            }
            QPushButton:hover { background-color: #45a049; }
        """)
        update_button.clicked.connect(self.update_order)
        
        time_layout.addWidget(time_label)
        time_layout.addWidget(self.time_input)
        time_layout.addWidget(update_button)
        
        layout.addWidget(title)
        layout.addLayout(time_layout)
        layout.addStretch()
        
        return right_content
        
    def update_order(self):
        """更新订单信息"""
        try:
            response = requests.post(
                f"{self.api_base_url}/update-order",
                json={"username": self.username},
                headers={'Content-Type': 'application/json'},
                timeout=5
            )
            
            if response.status_code == 200:
                QMessageBox.information(self, "成功", "库存信息更新成功！")
            else:
                QMessageBox.warning(self, "错误", "库存信息更新失败！")
                
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "错误", f"更新失败: {str(e)}")