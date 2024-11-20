from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFrame,
    QGroupBox,
    QMessageBox
)
from PyQt6.QtCore import Qt
import requests

class MainWindow(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.api_base_url = "http://localhost:8080/v1/shopee"
        self.setup_ui()
        
    def setup_ui(self):
        """设置UI界面"""
        self.setWindowTitle("Shopee Tools")
        self.setFixedSize(800, 600)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(30, 30, 30, 30)
        
        # 添加标题
        title_label = QLabel("Shopee Tools 主控面板")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 24px;
                font-weight: bold;
                color: #2c3e50;
                padding: 10px;
                background-color: #ecf0f1;
                border-radius: 5px;
            }
        """)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 添加用户信息
        user_info = QLabel(f"当前用户: {self.username}")
        user_info.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #7f8c8d;
                padding: 5px;
            }
        """)
        
        # 创建功能区域
        function_frame = QFrame()
        function_frame.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border: 2px solid #bdc3c7;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        function_layout = QVBoxLayout(function_frame)
        
        # 添加出货时间设置区域
        time_group = QGroupBox("出货时间设置")
        time_group.setStyleSheet("""
            QGroupBox {
                font-size: 18px;
                font-weight: bold;
                color: #2c3e50;
                border: 2px solid #3498db;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 10px;
                background-color: #ffffff;
            }
        """)
        
        time_layout = QVBoxLayout(time_group)
        
        # 添加时间输入框
        time_input_layout = QHBoxLayout()
        time_label = QLabel("设置时间:")
        time_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #34495e;
                min-width: 80px;
            }
        """)
        
        self.time_input = QLineEdit()
        self.time_input.setPlaceholderText("请输入出货时间")
        self.time_input.setMinimumHeight(40)
        self.time_input.setStyleSheet("""
            QLineEdit {
                font-size: 16px;
                padding: 5px 10px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                background-color: #f9f9f9;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background-color: #ffffff;
            }
        """)
        
        time_input_layout.addWidget(time_label)
        time_input_layout.addWidget(self.time_input)
        
        # 添加更新按钮
        update_button = QPushButton("更新库存信息")
        update_button.setMinimumHeight(45)
        update_button.setCursor(Qt.CursorShape.PointingHandCursor)
        update_button.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                color: white;
                background-color: #2ecc71;
                border: none;
                border-radius: 5px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            QPushButton:pressed {
                background-color: #219a52;
            }
        """)
        update_button.clicked.connect(self.update_order)
        
        # 添加状态显示区域
        self.status_label = QLabel()
        self.status_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                color: #7f8c8d;
                padding: 5px;
                min-height: 20px;
            }
        """)
        
        # 组装时间设置区域
        time_layout.addLayout(time_input_layout)
        time_layout.addWidget(update_button)
        time_layout.addWidget(self.status_label)
        
        # 添加所有组件到主布局
        main_layout.addWidget(title_label)
        main_layout.addWidget(user_info)
        main_layout.addWidget(function_frame)
        function_layout.addWidget(time_group)
        main_layout.addStretch()
        
    def update_order(self):
        """更新库存信息"""
        time_value = self.time_input.text().strip()
        if not time_value:
            self.status_label.setText("请输入出货时间！")
            self.status_label.setStyleSheet("color: #e74c3c;")  # 红色错误提示
            return
            
        try:
            response = requests.post(
                f"{self.api_base_url}/update-order",
                json={"username": self.username},
                headers={'Content-Type': 'application/json'},
                timeout=5
            )
            
            if response.status_code == 200:
                self.status_label.setText("库存信息更新成功！")
                self.status_label.setStyleSheet("color: #27ae60;")  # 绿色成功提示
            else:
                self.status_label.setText(f"更新失败: 服务器错误 ({response.status_code})")
                self.status_label.setStyleSheet("color: #e74c3c;")
                
        except requests.exceptions.RequestException as e:
            self.status_label.setText(f"更新失败: {str(e)}")
            self.status_label.setStyleSheet("color: #e74c3c;")