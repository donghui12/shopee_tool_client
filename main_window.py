from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QPushButton, QLabel, QFrame)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QFont

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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
        
        # 创建左侧菜单
        left_menu = QFrame()
        left_menu.setFixedWidth(200)
        left_menu.setStyleSheet("""
            QFrame {
                background-color: #2C2C2C;
                border: none;
            }
        """)
        
        # 左侧菜单布局
        left_layout = QVBoxLayout(left_menu)
        left_layout.setContentsMargins(0, 0, 0, 0)
        left_layout.setSpacing(0)
        
        # 添加菜单按钮
        menu_buttons = ['首页', '商品管理', '订单管理', '数据统计', '设置']
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
                QPushButton:hover {
                    background-color: #3C3C3C;
                }
                QPushButton:pressed {
                    background-color: #4CAF50;
                }
            """)
            left_layout.addWidget(btn)
        
        left_layout.addStretch()
        
        # 创建右侧内容区
        right_content = QFrame()
        right_content.setStyleSheet("""
            QFrame {
                background-color: #F5F5F5;
                border: none;
            }
        """)
        
        # 添加到主布局
        main_layout.addWidget(left_menu)
        main_layout.addWidget(right_content)