from PyQt6.QtWidgets import (
    QWidget, 
    QLabel, 
    QLineEdit, 
    QPushButton, 
    QVBoxLayout, 
    QHBoxLayout, 
    QMessageBox, 
    QFrame,
    QDialog
)
from vcode_dialog import VCodeDialog
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QPixmap, QFont
import requests
import json
import uuid
import platform
import subprocess
import os
import hashlib

# 激活码对话框类
class ActiveCodeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("激活码验证")
        self.setFixedSize(300, 150)
        
        layout = QVBoxLayout()
        
        label = QLabel("请输入激活码:")
        label.setStyleSheet("font-size: 14px; margin-bottom: 10px;")
        
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
        """)
        
        button_layout = QHBoxLayout()
        
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
        """)
        confirm_button.clicked.connect(self.accept)
        
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

# 登录窗口类
class LoginWindow(QWidget):
    def __init__(self, shopee_tools):
        super().__init__()
        self.shopee_tools = shopee_tools
        self.api_base_url = "http://localhost:8080/v1/shopee"
        self.username = ""
        self.machine_code = self.get_machine_code()
        self.vcode = ""
        self.setup_ui()

    def get_machine_code(self):
        """获取机器唯一标识码"""
        try:
            # 获取主板序列号或其他硬件信息
            if platform.system() == "Windows":
                command = "wmic baseboard get serialnumber"
                result = subprocess.check_output(command, shell=True).decode()
                serial = result.split('\n')[1].strip()
            else:  # macOS/Linux
                if platform.system() == "Darwin":  # macOS
                    command = "system_profiler SPHardwareDataType | grep 'Hardware UUID'"
                    result = subprocess.check_output(command, shell=True).decode()
                    serial = result.split(': ')[1].strip()
                else:  # Linux
                    try:
                        with open('/sys/class/dmi/id/board_serial') as f:
                            serial = f.read().strip()
                    except:
                        serial = str(uuid.uuid4())
            
            return hashlib.md5(serial.encode()).hexdigest()
            
        except Exception as e:
            print(f"获取机器码失败: {str(e)}")
            return hashlib.md5(str(uuid.uuid4()).encode()).hexdigest()

    def verify_machine_code(self):
        """验证机器码"""
        print(f"机器码: {self.machine_code}, 用户名: {self.username}")
        try:
            # 检查机器码是否已经绑定
            check_response = requests.get(
                f"{self.api_base_url}/mechine_code",
                params={
                    "machine_code": self.machine_code,
                    "username": self.username,
                },
                timeout=5
            )
            
            if check_response.status_code == 200:
                return True
                
            # 如果未绑定，尝试绑定机器码
            bind_response = requests.post(
                f"{self.api_base_url}/mechine_code",
                json={
                    "machine_code": self.machine_code,
                    "username": self.username
                },
                headers={'Content-Type': 'application/json'},
                timeout=5
            )
            
            return bind_response.status_code == 200
            
        except requests.exceptions.RequestException as e:
            print(f"验证机器码失败: {str(e)}")
            return False

    def setup_ui(self):
        """设置UI界面"""
        self.setWindowTitle('ShopeeTools - 登录')
        self.setFixedSize(400, 500)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
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
        login_layout.setContentsMargins(40, 40, 40, 40)
        
        # Logo
        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # 如果有logo图片，取消下面这行的注释并设置正确的路径
        # logo_label.setPixmap(QPixmap("path/to/logo.png").scaled(120, 120, Qt.AspectRatioMode.KeepAspectRatio))
        
        # 用户名输入框
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("用户名")
        self.username_input.setMinimumHeight(45)
        self.username_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 14px;
                margin-bottom: 10px;
            }
            QLineEdit:focus {
                border: 1px solid #4CAF50;
            }
        """)
        
        # 密码输入框
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("密码")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setMinimumHeight(45)
        self.password_input.setStyleSheet("""
            QLineEdit {
                border: 1px solid #CCCCCC;
                border-radius: 5px;
                padding: 5px 10px;
                font-size: 14px;
                margin-bottom: 20px;
            }
            QLineEdit:focus {
                border: 1px solid #4CAF50;
            }
        """)
        
        # 登录按钮
        self.login_button = QPushButton("登录")
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
    
    def show_vcode_dialog(self):
        """显示验证码输入对话框"""
        dialog = VCodeDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:  # 用户点击确定
            self.vcode = dialog.get_vcode()
            return True
        return False

    def handle_login(self):
        """处理登录"""
        username = self.username_input.text()
        password = self.password_input.text()
        
        login_data = {
            "username": username,
            "password": password
        }
        
        if self.vcode:
            login_data["vcode"] = self.vcode
        
        try:
            response = requests.post(
                f"{self.api_base_url}/login", 
                json=login_data,
                headers={'Content-Type': 'application/json'},
                timeout=5
            )
            
            print("状态码:", response.status_code)
            print("响应内容:", response.text)
            
            if response.status_code == 200:
                result = response.json()
                
                # 检查是否需要验证码
                if result.get('code') == 410 and "需要验证码" in result.get('message', ''):
                    if self.show_vcode_dialog():
                        self.handle_login()
                    return
                
                if result.get('code') == 410 and "验证码错误" in result.get('message', ''):
                    QMessageBox.warning(self, "错误", "验证码错误！")
                    self.vcode = ""
                    self.handle_login()
                    return
                
                if result.get('code') == 200:  # 登录成功
                    self.username = username
                    # 验证机器码
                    if not self.verify_machine_code():
                        QMessageBox.warning(self, "警告", "机器码验证失败！")
                        return
                    
                    # 验证激活码
                    if not self.verify_and_bind_active_code(username):
                        return
                    
                    QMessageBox.information(self, "成功", "登录成功！")
                    self.shopee_tools.show_main_window(username)
                else:
                    error_msg = result.get('message', '登录失败！')
                    QMessageBox.warning(self, "错误", error_msg)
                    self.vcode = ""
            else:
                QMessageBox.warning(self, "错误", f"服务器错误: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "错误", f"请求错误: {str(e)}")

    def verify_and_bind_active_code(self, username):
        """验证并绑定激活码"""
        while True:  # 循环直到成功或用户取消
            try:
                active_response = requests.get(
                    f"{self.api_base_url}/active_code",
                    params={"username": username},
                    timeout=5
                )
                
                print("激活码验证响应:", active_response.text)
                
                if active_response.status_code == 200:
                    return True  # 激活码验证成功
                    
                # 显示激活码输入对话框
                active_dialog = ActiveCodeDialog(self)
                if active_dialog.exec() != 1:  # 用户点击取消
                    return False
                    
                active_code = active_dialog.get_active_code()
                verify_active_code_response = requests.get(
                        f"{self.api_base_url}/verify_active_code",
                        params={"active_code": active_code},
                        timeout=5
                    )

                if verify_active_code_response.status_code != 200:
                    QMessageBox.warning(self, "错误", "无效激活码！")
                    continue

                # 绑定激活码
                bind_response = requests.post(
                    f"{self.api_base_url}/bind_active_code",
                    json={
                        "username": username,
                        "active_code": active_code
                    },
                    headers={'Content-Type': 'application/json'},
                    timeout=5
                )
                
                print("绑定激活码响应:", bind_response.text)
                
                if bind_response.status_code == 200:
                    return True
                else:
                    QMessageBox.warning(
                        self, 
                        "错误", 
                        f"激活码绑定失败（{bind_response.status_code}），请重新输入！"
                    )
                    continue  # 继续循环，重新输入
                    
            except requests.exceptions.RequestException as e:
                QMessageBox.critical(self, "错误", f"验证激活码失败: {str(e)}")
                retry = QMessageBox.question(
                    self,
                    "重试",
                    "网络错误，是否重试？",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if retry == QMessageBox.StandardButton.Yes:
                    continue  # 继续循环，重试
                return False  # 用户选择不重试

    def mousePressEvent(self, event):
        """实现窗口拖动"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        """实现窗口拖动"""
        if event.buttons() == Qt.MouseButton.LeftButton and self.dragging:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        """实现窗口拖动"""
        self.dragging = False