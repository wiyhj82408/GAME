

import sys
import random
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QPushButton, QLabel, QTextEdit, QListWidgetItem
)
from PySide6.QtCore import Qt


DEFAULT_CATEGORIES = [
    "1","2","3","4"
]

DEFAULT_ZHUYIN = "1 2 3 4 5 6 7 8 9 "


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("test")
        self.resize(580, 460)

        main = QWidget()
        self.setCentralWidget(main)
        v = QVBoxLayout(main)

        # --- 題目列表 ---
        self.cat_list = QListWidget()
        self.cat_list.addItems(DEFAULT_CATEGORIES)
        v.addWidget(self.cat_list, 2)

        # --- 按鈕 ---
        btn_draw_cat = QPushButton("test")
        btn_draw_cat.setStyleSheet("font-size: 18px; padding: 10px;")
        v.addWidget(btn_draw_cat)

        # --- 中間：顯示結果 ---
        self.result_cat_label = QLabel("test")
        self.result_cat_label.setAlignment(Qt.AlignCenter)
        self.result_cat_label.setStyleSheet("font-size: 22px; padding: 8px; border: 1px solid #ccc; border-radius:8px;")

        self.result_zh_label = QLabel("test")
        self.result_zh_label.setAlignment(Qt.AlignCenter)
        self.result_zh_label.setStyleSheet("font-size: 22px; padding: 8px; border: 1px solid #ccc; border-radius:8px;")

        v.addWidget(self.result_cat_label)
        v.addWidget(self.result_zh_label)

        # --- 注音管理 ---
        v.addWidget(QLabel("test"))
        self.zh_text = QTextEdit()
        self.zh_text.setPlainText(DEFAULT_ZHUYIN)
        v.addWidget(self.zh_text)

        zh_btn_row = QHBoxLayout()
        self.btn_apply_zh = QPushButton("test")
        self.btn_draw_zh = QPushButton("test 🎯")
        self.btn_apply_zh.setStyleSheet("font-size: 16px; padding: 8px;")
        self.btn_draw_zh.setStyleSheet("font-size: 16px; padding: 8px;")
        zh_btn_row.addWidget(self.btn_apply_zh)
        zh_btn_row.addWidget(self.btn_draw_zh)
        v.addLayout(zh_btn_row)

        # --- 歷史 ---
        v.addWidget(QLabel("test"))
        self.last_items = QListWidget()
        v.addWidget(self.last_items)

        # --- 事件綁定 ---
        btn_draw_cat.clicked.connect(self.draw_category)
        self.btn_apply_zh.clicked.connect(self.apply_zhuyin)
        self.btn_draw_zh.clicked.connect(self.draw_zhuyin)

        self.zhuoyin_list = self._parse_zhuyin_text(self.zh_text.toPlainText())

    def draw_category(self):
        count = self.cat_list.count()
        if count == 0:
            return
        idx = random.randrange(count)
        text = self.cat_list.item(idx).text()
        self.result_cat_label.setText(f"test{text}")
        self._push_history(f"test{text}")

    def _parse_zhuyin_text(self, raw: str):
        parts = []
        for line in raw.splitlines():
            for token in line.replace(',', ' ').split():
                token = token.strip()
                if token:
                    parts.append(token)
        return parts

    def apply_zhuyin(self):
        raw = self.zh_text.toPlainText()
        parsed = self._parse_zhuyin_text(raw)
        if not parsed:
            return
        self.zhuoyin_list = parsed

    def draw_zhuyin(self):
        if not self.zhuoyin_list:
            return
        chosen = random.choice(self.zhuoyin_list)
        self.result_zh_label.setText(f"test：{chosen}")
        self._push_history(f"test：{chosen}")

    def _push_history(self, text: str):
        self.last_items.insertItem(0, QListWidgetItem(text))
        if self.last_items.count() > 20:
            item = self.last_items.takeItem(self.last_items.count() - 1)
            del item


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())