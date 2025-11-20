import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QVBoxLayout,QHBoxLayout, QPushButton, QLabel, QStackedWidget, QGroupBox
from PySide6.QtCore import Qt

class MainMenuWidget(QWidget):
    
    def __init__(self, main_window: QMainWindow, parent=None):
        super().__init__(parent)
        self.main_window = main_window
        
        main_layout = QVBoxLayout(self)
        
        # タイトル
        title_label = QLabel("メニュー")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24pt; margin-bottom: 30px;")
        main_layout.addWidget(title_label)
        
        # ボタンを配置するグループボックス
        button_group_box = QGroupBox("機能選択")
        v_layout = QVBoxLayout(button_group_box)
        
        # 写真撮影ボタン
        self.camera_button = QPushButton("写真撮影")
        self.camera_button.clicked.connect(self.main_window.show_camera)
        self.camera_button.setFixedSize(250, 60)

        # 画像合成ボタン
        self.composite_button = QPushButton("画像合成")
        self.composite_button.clicked.connect(self.main_window.show_composite)
        self.composite_button.setFixedSize(250, 60)
        self.composite_button.setEnabled(False) 

        v_layout.addWidget(self.camera_button)
        v_layout.addWidget(self.composite_button)
        v_layout.setAlignment(Qt.AlignmentFlag.AlignCenter) 

        main_layout.addWidget(button_group_box, alignment=Qt.AlignmentFlag.AlignCenter)

        self.status_label = QLabel("画像: なし")
        self.status_label.setStyleSheet("margin-top: 20px;")
        main_layout.addWidget(self.status_label, alignment=Qt.AlignmentFlag.AlignCenter)
        
        main_layout.addStretch()
        
    def set_composite_status(self, is_available: bool):
        self.composite_button.setEnabled(is_available)
        if is_available:
            self.status_label.setText("画像: あり ")
        else:
            self.status_label.setText("画像: なし")

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("カメラ/合成アプリ")
        self.setGeometry(100, 100, 800, 600)
        
        self.has_captured_frame: bool = False 

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.menu_widget = MainMenuWidget(self)
        self.camera_widget =
        self.composite_widget =

        self.stacked_widget.addWidget(self.menu_widget)    # Index 0
        self.stacked_widget.addWidget(self.camera_widget)  # Index 1
        self.stacked_widget.addWidget(self.composite_widget) # Index 2

        self.show_menu()

    def show_menu(self):
        """メインメニュー画面を表示する (Index 0)。"""
        self.stacked_widget.setCurrentIndex(0)
        self.menu_widget.set_composite_status(self.has_captured_frame)

    def show_camera(self):
        """写真撮影画面を表示する (Index 1)。"""
        self.stacked_widget.setCurrentIndex(1)
        
    def show_composite(self):
        """画像合成画面を表示する (Index 2)。"""
        if self.has_captured_frame:
            self.stacked_widget.setCurrentIndex(2)

    def sim_capture_and_show_menu(self):
        self.has_captured_frame = True 
        self.show_menu()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())