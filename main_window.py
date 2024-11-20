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
        self.time_input.setPlaceholderText("请输入出货时间（1-365天）")
        self.time_input.setMinimumHeight(40)
        self.time_input.textChanged.connect(self.validate_input)
        self.time_input.setStyleSheet("""
            QLineEdit {
                font-size: 16px;
                padding: 5px 15px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                background-color: white;
                color: #2c3e50;
                font-weight: 500;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background-color: #f8f9fa;
            }
            QLineEdit::placeholder {
                color: #95a5a6;
                font-weight: normal;
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
        
        # 验证输入是否为空
        if not time_value:
            QMessageBox.warning(
                self,
                "输入错误",
                "请输入出货时间！",
                QMessageBox.StandardButton.Ok
            )
            self.status_label.setText("请输入出货时间！")
            self.status_label.setStyleSheet("color: #e74c3c;")
            return
        
        # 验证输入是否为数字
        try:
            days = int(time_value)
        except ValueError:
            QMessageBox.warning(
                self,
                "输入错误",
                "请输入有效的数字！",
                QMessageBox.StandardButton.Ok
            )
            self.status_label.setText("请输入有效的数字！")
            self.status_label.setStyleSheet("color: #e74c3c;")
            return
        
        # 验证天数范围
        if days <= 0 or days > 365:
            QMessageBox.warning(
                self,
                "输入错误",
                "出货时间必须在 1-365 天之间！",
                QMessageBox.StandardButton.Ok
            )
            self.status_label.setText("出货时间必须在 1-365 天之间！")
            self.status_label.setStyleSheet("color: #e74c3c;")
            return
            
        try:
            response = requests.post(
                f"{self.api_base_url}/update_order",
                json={
                    "username": self.username,
                    "day": days  # 添加天数参数
                },
                headers={'Content-Type': 'application/json'},
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('code') == 200:
                    QMessageBox.information(
                        self,
                        "成功",
                        "库存信息更新成功！",
                        QMessageBox.StandardButton.Ok
                    )
                    self.status_label.setText("库存信息更新成功！")
                    self.status_label.setStyleSheet("color: #27ae60;")  # 绿色成功提示
                else:
                    error_msg = result.get('message', '更新失败')
                    QMessageBox.warning(
                        self,
                        "错误",
                        f"更新失败: {error_msg}",
                        QMessageBox.StandardButton.Ok
                    )
                    self.status_label.setText(f"更新失败: {error_msg}")
                    self.status_label.setStyleSheet("color: #e74c3c;")
            else:
                QMessageBox.warning(
                    self,
                    "错误",
                    f"服务器错误 ({response.status_code})",
                    QMessageBox.StandardButton.Ok
                )
                self.status_label.setText(f"更新失败: 服务器错误 ({response.status_code})")
                self.status_label.setStyleSheet("color: #e74c3c;")
                
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(
                self,
                "错误",
                f"网络错误: {str(e)}",
                QMessageBox.StandardButton.Ok
            )
            self.status_label.setText(f"更新失败: {str(e)}")
            self.status_label.setStyleSheet("color: #e74c3c;")

    def validate_input(self, text):
        """实时验证输入"""
        if text:
            try:
                days = int(text)
                if days <= 0 or days > 365:
                    self.time_input.setStyleSheet("""
                        QLineEdit {
                            font-size: 16px;
                            padding: 5px 15px;
                            border: 2px solid #e74c3c;
                            border-radius: 5px;
                            background-color: white;
                            color: #2c3e50;
                            font-weight: 500;
                        }
                    """)
                    self.status_label.setText("出货时间必须在1-365天之间！")
                    self.status_label.setStyleSheet("color: #e74c3c;")
                else:
                    self.time_input.setStyleSheet("""
                        QLineEdit {
                            font-size: 16px;
                            padding: 5px 15px;
                            border: 2px solid #2ecc71;
                            border-radius: 5px;
                            background-color: white;
                            color: #2c3e50;
                            font-weight: 500;
                        }
                    """)
                    self.status_label.setText("输入有效")
                    self.status_label.setStyleSheet("color: #27ae60;")
            except ValueError:
                self.time_input.setStyleSheet("""
                    QLineEdit {
                        font-size: 16px;
                        padding: 5px 15px;
                        border: 2px solid #e74c3c;
                        border-radius: 5px;
                        background-color: white;
                        color: #2c3e50;
                        font-weight: 500;
                    }
                """)
                self.status_label.setText("请输入有效的数字！")
                self.status_label.setStyleSheet("color: #e74c3c;")
        else:
            # 输入框为空时恢复默认样式
            self.time_input.setStyleSheet("""
                QLineEdit {
                    font-size: 16px;
                    padding: 5px 15px;
                    border: 2px solid #bdc3c7;
                    border-radius: 5px;
                    background-color: white;
                    color: #2c3e50;
                    font-weight: 500;
                }
            """)
            self.status_label.setText("")