from PyQt6.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, 
                           QVBoxLayout, QHBoxLayout, QMessageBox, QFrame)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap, QFont
import requests
import json
import uuid
import platform
import subprocess
import os

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.api_base_url = "http://IP:8080/v1/shopee"
        self.username = ""
        self.machine_code = self.get_machine_code()
        self.setup_ui()
        
    def get_machine_code(self):
        """获取机器唯一标识码"""
        try:
            # 获取主板序列号
            if platform.system() == "Windows":
                command = "wmic baseboard get serialnumber"
                result = subprocess.check_output(command, shell=True).decode()
                motherboard_serial = result.split('\n')[1].strip()
            else:  # Linux/Mac
                command = "system_profiler SPHardwareDataType | grep 'Serial Number'"
                result = subprocess.check_output(command, shell=True).decode()
                motherboard_serial = result.split(':')[1].strip()
        except:
            motherboard_serial = ""

        # 获取CPU信息
        try:
            if platform.system() == "Windows":
                command = "wmic cpu get processorid"
                result = subprocess.check_output(command, shell=True).decode()
                processor_id = result.split('\n')[1].strip()
            else:  # Linux/Mac
                command = "sysctl -n machdep.cpu.brand_string"
                result = subprocess.check_output(command, shell=True).decode()
                processor_id = result.strip()
        except:
            processor_id = ""

        # 组合信息生成唯一标识
        machine_id = f"{motherboard_serial}_{processor_id}_{str(uuid.getnode())}"
        return uuid.uuid5(uuid.NAMESPACE_DNS, machine_id).hex
        
    def setup_ui(self):
        # 设置窗口基本属性
        self.setWindowTitle('ShopeeTools - 登录')
        self.setFixedSize(400, 500)  # 固定窗口大小
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)  # 无边框窗口
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # 透明背景
        
        # 创建主布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # 创建登录框
        login_frame = QFrame()
        login_frame.setObjectName("loginFrame")
        login_frame.setStyleSheet("""
            #loginFrame {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #CCCCCC;
            }
        """)
        
        # 登录框布局
        login_layout = QVBoxLayout()
        login_layout.setSpacing(15)
        login_layout.setContentsMargins(40, 30, 40, 40)
        
        # Logo
        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # 这里需要替换为你的实际logo路径
        # logo_pixmap = QPixmap("path/to/your/logo.png")
        # logo_label.setPixmap(logo_pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio))
        logo_label.setText("ShopeeTools")  # 临时使用文字代替logo
        logo_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        
        # 用户名输入框
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("用户名")
        self.username_input.setMinimumHeight(40)
        self.username_input.setStyleSheet("""
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
        
        # 密码输入框
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("密码")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(40)
        self.password_input.setStyleSheet(self.username_input.styleSheet())
        
        # 登录按钮
        self.login_button = QPushButton("登 录")
        self.login_button.setMinimumHeight(45)
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        self.login_button.clicked.connect(self.handle_login)
        
        # 添加组件到登录框布局
        login_layout.addWidget(logo_label)
        login_layout.addSpacing(20)
        login_layout.addWidget(self.username_input)
        login_layout.addWidget(self.password_input)
        login_layout.addSpacing(10)
        login_layout.addWidget(self.login_button)
        
        # 设置登录框布局
        login_frame.setLayout(login_layout)
        
        # 添加登录框到主布局
        main_layout.addStretch()
        main_layout.addWidget(login_frame)
        main_layout.addStretch()
        
        # 设置主布局
        self.setLayout(main_layout)

    def verify_machine_code(self):
        """验证或注册机器码"""
        try:
            response = requests.get(
                f"{self.api_base_url}/mechine_code",
                params={"machine_code": self.machine_code},
                timeout=5
            )
            
            if response.status_code != 200:
                # 如果获取失败，尝试注册新机器码
                register_data = {
                    "username": self.username,
                    "mechine_code": self.machine_code
                }
                
                response = requests.post(
                    f"{self.api_base_url}/mechine_code",
                    json=register_data,
                    headers={'Content-Type': 'application/json'},
                    timeout=5
                )
                
                if response.status_code != 200:
                    QMessageBox.critical(self, "错误", "机器码注册失败！")
                    return False
                    
            return True
            
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "错误", f"机器码验证失败: {str(e)}")
            return False

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        login_data = {
            "username": username,
            "password": password
        }
        
        try:
            response = requests.post(
                f"{self.api_base_url}/login", 
                json=login_data,
                headers={'Content-Type': 'application/json'},
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success', False):
                    self.username = username  # 保存用户名
                    # 登录成功后验证机器码
                    if self.verify_machine_code():
                        QMessageBox.information(self, "成功", "登录成功！")
                        # 这里可以添加登录成功后的操作
                    else:
                        QMessageBox.warning(self, "警告", "登录成功但机器码验证失败！")
                else:
                    QMessageBox.warning(self, "错误", result.get('message', '登录失败！'))
            else:
                QMessageBox.warning(self, "错误", f"服务器错误: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "错误", f"请求错误: {str(e)}")