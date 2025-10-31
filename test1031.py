from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt
import random
import sys

class DrawApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("🎲 抽籤小程式")
        self.setFixedSize(300, 200)

        # 候選項目
        self.options = ["吃火鍋", "看電影", "健身", "加班", "睡覺"]

        # 介面元件
        self.label = QLabel("按下按鈕開始抽籤", alignment=Qt.AlignCenter)
        self.button = QPushButton("開始抽籤")
        self.button.clicked.connect(self.draw_lottery)

        # 版面配置
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def draw_lottery(self):
        result = random.choice(self.options)
        self.label.setText(f"✨ 結果是：{result}！")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DrawApp()
    window.show()
    sys.exit(app.exec())
