import sys
import random
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QPushButton, QLineEdit, QLabel, QMessageBox

class SimpleDrawApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("簡單抽籤程式")
        self.resize(400, 300)

        layout = QVBoxLayout(self)

        # 顯示項目
        self.list_widget = QListWidget()
        layout.addWidget(QLabel("抽籤項目："))
        layout.addWidget(self.list_widget)

        # 輸入框 + 新增按鈕
        hbox = QHBoxLayout()
        self.input_line = QLineEdit()
        self.input_line.setPlaceholderText("輸入項目後按 Enter 或點新增")
        self.input_line.returnPressed.connect(self.add_item)
        hbox.addWidget(self.input_line)
        btn_add = QPushButton("新增")
        btn_add.clicked.connect(self.add_item)
        hbox.addWidget(btn_add)
        layout.addLayout(hbox)

        # 操作按鈕
        btn_draw = QPushButton("抽一個")
        btn_draw.clicked.connect(self.do_draw)
        layout.addWidget(btn_draw)

        btn_remove = QPushButton("刪除選取")
        btn_remove.clicked.connect(self.remove_item)
        layout.addWidget(btn_remove)

    def add_item(self):
        text = self.input_line.text().strip()
        if text:
            self.list_widget.addItem(text)
            self.input_line.clear()

    def remove_item(self):
        row = self.list_widget.currentRow()
        if row >= 0:
            self.list_widget.takeItem(row)

    def do_draw(self):
        count = self.list_widget.count()
        if count == 0:
            QMessageBox.warning(self, "沒有項目", "請先新增項目再抽籤！")
            return
        items = [self.list_widget.item(i).text() for i in range(count)]
        choice = random.choice(items)
        QMessageBox.information(self, "抽籤結果", f"抽到：{choice}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = SimpleDrawApp()
    win.show()
    sys.exit(app.exec())
