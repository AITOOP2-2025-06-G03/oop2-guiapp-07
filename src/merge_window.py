import cv2
import numpy as np
from PySide6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QMessageBox
from PySide6.QtGui import QPixmap, QImage


def composite_image(base_img, capture_img):
    """白色部分をカメラ画像で置換した合成処理"""

    h, w, _ = base_img.shape
    ch, cw, _ = capture_img.shape

    out = base_img.copy()

    for y in range(h):
        for x in range(w):
            b, g, r = base_img[y, x]
            if (b, g, r) == (255, 255, 255):
                out[y, x] = capture_img[y % ch, x % cw]

    return out


class CompositeWindow(QWidget):
    """画像合成プレビュー＆保存ウィンドウ"""

    def __init__(self, base_img_path="images/google.png", capture_img_path=None):
        super().__init__()
        self.setWindowTitle("画像合成プレビュー")

        # 読み込み
        self.base_img = cv2.imread(base_img_path)
        if capture_img_path is None:
            QMessageBox.warning(self, "エラー", "撮影画像がありません。")
            return

        self.capture_img = cv2.imread(capture_img_path)

        # 合成処理
        self.result_img = composite_image(self.base_img, self.capture_img)

        # GUIレイアウト
        self.preview_label = QLabel()
        self.preview_label.setPixmap(self.to_pixmap(self.result_img))

        self.save_button = QPushButton("保存する")
        self.save_button.clicked.connect(self.save_image)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("合成プレビュー"))
        layout.addWidget(self.preview_label)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def to_pixmap(self, img):
        """OpenCV画像 → Qt表示用に変換"""
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w, ch = img_rgb.shape
        qimg = QImage(img_rgb.data, w, h, ch * w, QImage.Format_RGB888)
        return QPixmap.fromImage(qimg)

    def save_image(self):
        """結果画像を保存"""
        save_path = "output_images/result.png"
        cv2.imwrite(save_path, self.result_img)
        QMessageBox.information(self, "保存完了", f"保存しました：{save_path}")
