

import sys
import random
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QPushButton, QLabel, QTextEdit, QListWidgetItem
)
from PySide6.QtCore import Qt


DEFAULT_CATEGORIES = [
    "學校裡的東西", "生日會有的東西", "名字有三個字的東西", "名字聽起來很好吃的東西",
    "每天都會用到的東西", "會滾的東西", "兩個字的歌名", "天上會飛的動物",
    "水裡的動物", "越大越不方便的東西", "名字裡有動物的東西", "可以吹的東西",
    "越快越危險的東西", "職業", "名字會重疊的東西", "公園裡的東西", "會讓人開心的東西",
    "出門會帶的東西", "房間裡會看到的東西", "越洗越乾淨的東西", "沒腳的動物",
    "名字有聲音的東西", "車上會有的東西", "中秋節會看到的東西", "越用越少的東西",
    "夜行性的動物", "可以丟的東西", "四隻腳的動物", "端午節會出現的東西",
    "名字聽起來很危險的東西", "會動的東西", "足球選手", "可以堆起來的東西", "名字裡有顏色的東西",
    "兩隻腳的動物", "沒有形狀的東西", "用來運輸的東西", "廟會常見的東西",
    "放在冰箱裡的東西", "男歌手", "有名字的東西", "不能吃的東西",
    "三個字的歌名", "可以飛的東西", "啦啦隊員", "過年的東西", "有毛的動物",
    "小孩子會玩的東西", "會發出聲音的東西", "可以聽到的東西", "聖誕節會看到的東西",
    "洗澡會用到的東西", "常會壞掉的東西", "玩具店會有的東西", "跟時間有關的東西",
    "廚房裡的東西", "女歌手", "有尾巴的動物", "馬路上會看到的東西",
    "看不到但感覺得到的東西", "四個字的歌名", "有顏色的東西", "五個字的歌名", "棒球選手"
]

DEFAULT_ZHUYIN = "ㄅ ㄆ ㄇ ㄈ ㄉ ㄊ ㄋ ㄌ ㄍ ㄎ ㄏ ㄐ ㄑ ㄒ ㄓ ㄔ ㄕ ㄖ ㄗ ㄘ ㄙ ㄧ ㄨ ㄩ ㄚ ㄛ ㄜ ㄝ ㄞ ㄟ ㄠ ㄡ ㄢ ㄣ ㄤ ㄥ ㄦ"


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("抽題目與注音小工具")
        self.resize(580, 460)

        main = QWidget()
        self.setCentralWidget(main)
        v = QVBoxLayout(main)

        # --- 題目列表 ---
        self.cat_list = QListWidget()
        self.cat_list.addItems(DEFAULT_CATEGORIES)
        v.addWidget(self.cat_list, 2)

        # --- 按鈕 ---
        btn_draw_cat = QPushButton("抽一個題目 🎲")
        btn_draw_cat.setStyleSheet("font-size: 18px; padding: 10px;")
        v.addWidget(btn_draw_cat)

        # --- 中間：顯示結果 ---
        self.result_cat_label = QLabel("題目：尚未抽出")
        self.result_cat_label.setAlignment(Qt.AlignCenter)
        self.result_cat_label.setStyleSheet("font-size: 22px; padding: 8px; border: 1px solid #ccc; border-radius:8px;")

        self.result_zh_label = QLabel("注音：尚未抽出")
        self.result_zh_label.setAlignment(Qt.AlignCenter)
        self.result_zh_label.setStyleSheet("font-size: 22px; padding: 8px; border: 1px solid #ccc; border-radius:8px;")

        v.addWidget(self.result_cat_label)
        v.addWidget(self.result_zh_label)

        # --- 注音管理 ---
        v.addWidget(QLabel("注音集合（以空白、逗號或換行分隔，可直接修改）"))
        self.zh_text = QTextEdit()
        self.zh_text.setPlainText(DEFAULT_ZHUYIN)
        v.addWidget(self.zh_text)

        zh_btn_row = QHBoxLayout()
        self.btn_apply_zh = QPushButton("套用注音")
        self.btn_draw_zh = QPushButton("抽注音 🎯")
        self.btn_apply_zh.setStyleSheet("font-size: 16px; padding: 8px;")
        self.btn_draw_zh.setStyleSheet("font-size: 16px; padding: 8px;")
        zh_btn_row.addWidget(self.btn_apply_zh)
        zh_btn_row.addWidget(self.btn_draw_zh)
        v.addLayout(zh_btn_row)

        # --- 歷史 ---
        v.addWidget(QLabel("最近抽到的項目"))
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
        self.result_cat_label.setText(f"題目：{text}")
        self._push_history(f"題目：{text}")

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
        self.result_zh_label.setText(f"注音：{chosen}")
        self._push_history(f"注音：{chosen}")

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