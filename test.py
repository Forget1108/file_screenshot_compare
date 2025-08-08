# gui_main.py
import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QLabel, QTextEdit, 
                             QFileDialog, QMessageBox, QAction, QDialog, QVBoxLayout, QLabel)
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import Qt
from capture import capture_image
from compare import compare_two_image
import cv2
import numpy as np

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('功能介绍')
        self.setGeometry(200, 200, 600, 400)
        
        layout = QVBoxLayout()
        
        # 添加文本介绍
        text_label = QLabel(self)
        text_label.setText(
            "这是一个文件夹对比工具，可以通过截图两个文件夹目录并进行对比。\n"
            "主要功能包括：\n"
            "1. 截图两个文件夹目录\n"
            "2. 对比两个文件夹中的文件\n"
            "3. 显示对比结果\n"
        )
        text_label.setWordWrap(True)  # 自动换行
        layout.addWidget(text_label)
        
        # 添加图片
        image_label = QLabel(self)
        pixmap = QPixmap("path_to_your_image.png")  # 替换为你的图片路径
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(image_label)
        
        self.setLayout(layout)

class FileCompareGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.image1_path = None
        self.image2_path = None
        self.init_ui()
    
    def init_ui(self):
        """初始化UI界面"""
        self.setWindowTitle('文件夹对比工具')
        self.setGeometry(100, 100, 1200, 800)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 图片展示区域
        images_layout = QHBoxLayout()
        
        # 第一个图片展示框
        self.image1_widget = QWidget()
        image1_layout = QVBoxLayout(self.image1_widget)
        
        self.image1_label = QLabel('第一个截图')
        self.image1_label.setAlignment(Qt.AlignCenter)
        self.image1_label.setMinimumSize(400, 300)
        self.image1_label.setStyleSheet("border: 1px solid black;")
        
        self.capture1_button = QPushButton('截图第一个文件夹')
        self.capture1_button.clicked.connect(self.capture_first_image)
        
        image1_layout.addWidget(self.image1_label)
        image1_layout.addWidget(self.capture1_button)
        
        # 第二个图片展示框
        self.image2_widget = QWidget()
        image2_layout = QVBoxLayout(self.image2_widget)
        
        self.image2_label = QLabel('第二个截图')
        self.image2_label.setAlignment(Qt.AlignCenter)
        self.image2_label.setMinimumSize(400, 300)
        self.image2_label.setStyleSheet("border: 1px solid black;")
        
        self.capture2_button = QPushButton('截图第二个文件夹')
        self.capture2_button.clicked.connect(self.capture_second_image)
        
        image2_layout.addWidget(self.image2_label)
        image2_layout.addWidget(self.capture2_button)
        
        images_layout.addWidget(self.image1_widget)
        images_layout.addWidget(self.image2_widget)
        
        # 对比按钮区域（缩小空间）
        button_layout = QHBoxLayout()
        self.compare_button = QPushButton('对比两个文件夹')
        self.compare_button.clicked.connect(self.compare_images)
        self.compare_button.setEnabled(False)  # 初始禁用，直到两个图片都加载
        
        button_layout.addWidget(self.compare_button)
        
        # 结果输出区域（放大空间）
        result_layout = QVBoxLayout()
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setMinimumHeight(400)  # 增加高度
        self.result_text.setPlaceholderText("对比结果将显示在这里...")
        
        result_layout.addWidget(QLabel('对比结果:'))
        result_layout.addWidget(self.result_text)
        
        # 添加到主布局
        main_layout.addLayout(images_layout)
        main_layout.addLayout(button_layout)
        main_layout.addLayout(result_layout)
        
        # 在标题栏右侧添加问号按钮
        self.about_action = QAction(self)
        self.about_action.setIcon(QIcon("D:\file_compare_scan\picture\1754545964909.jpg"))  # 替换为你的图标路径
        self.about_action.triggered.connect(self.show_about_dialog)
        self.addAction(self.about_action)
        
        # 设置窗口控件
        self.setWindowFlags(self.windowFlags() | Qt.WindowContextHelpButtonHint)
        self.setWindowIcon(QIcon("D:\file_compare_scan\picture\1754545964909.jpg"))  # 替换为你的图标路径
    
    def capture_first_image(self):
        """截图第一个图片"""
        try:
            self.result_text.append("正在截图第一个文件夹...")
            QApplication.processEvents()  # 更新界面
            
            image_path = capture_image()
            if image_path and os.path.exists(image_path):
                self.image1_path = image_path
                self.display_image(image_path, self.image1_label)
                self.result_text.append(f"第一个截图完成: {image_path}")
                self.check_compare_button()
            else:
                self.result_text.append("第一个截图取消或失败")
        except Exception as e:
            self.result_text.append(f"截图第一个图片时出错: {str(e)}")
    
    def capture_second_image(self):
        """截图第二个图片"""
        try:
            self.result_text.append("正在截图第二个文件夹...")
            QApplication.processEvents()  # 更新界面
            
            image_path = capture_image()
            if image_path and os.path.exists(image_path):
                self.image2_path = image_path
                self.display_image(image_path, self.image2_label)
                self.result_text.append(f"第二个截图完成: {image_path}")
                self.check_compare_button()
            else:
                self.result_text.append("第二个截图取消或失败")
        except Exception as e:
            self.result_text.append(f"截图第二个图片时出错: {str(e)}")
    
    def display_image(self, image_path, label):
        """在指定标签中显示图片"""
        try:
            # 读取图片
            pixmap = QPixmap(image_path)
            
            # 缩放图片以适应标签
            pixmap = pixmap.scaled(
                label.width(), 
                label.height(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            
            label.setPixmap(pixmap)
        except Exception as e:
            self.result_text.append(f"显示图片时出错: {str(e)}")
    
    def check_compare_button(self):
        """检查对比按钮是否应该启用"""
        if self.image1_path and self.image2_path:
            self.compare_button.setEnabled(True)
        else:
            self.compare_button.setEnabled(False)
    
    def compare_images(self):
        """对比两个图片"""
        if not self.image1_path or not self.image2_path:
            QMessageBox.warning(self, "警告", "请先截取两个文件夹的图片")
            return
        
        try:
            self.result_text.append("开始对比两个文件夹...")
            self.result_text.append("="*50)
            QApplication.processEvents()  # 更新界面
            
            # 重定向compare_two_image的输出到文本框
            from io import StringIO
            import sys
            
            old_stdout = sys.stdout
            sys.stdout = StringIO()
            
            try:
                compare_two_image(self.image1_path, self.image2_path)
                output = sys.stdout.getvalue()
                self.result_text.append(output)
            finally:
                sys.stdout = old_stdout
                
        except Exception as e:
            self.result_text.append(f"对比过程中出错: {str(e)}")

    def show_about_dialog(self):
        """显示关于对话框"""
        dialog = AboutDialog(self)
        dialog.exec_()

def main():
    app = QApplication(sys.argv)
    window = FileCompareGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()