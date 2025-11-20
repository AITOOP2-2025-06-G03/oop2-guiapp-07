import numpy as np
import cv2


class MyVideoCapture:
    """Webカメラから映像を取得し、中心にターゲットマークを描画して表示・保存するクラス。

    Attributes:
        DELAY (int): 各フレームの表示間隔（ミリ秒）。
        cap (cv2.VideoCapture): OpenCVのビデオキャプチャオブジェクト。
        captured_img (np.ndarray | None): 最後にキャプチャされた画像データ。
    """

    DELAY: int = 100  # 100 msecのディレイ

    def __init__(self) -> None:
        """Webカメラを初期化する。

        Notes:
            PCによってはカメラIDが0ではなく1で動作する場合があるため、
            必要に応じて cv2.VideoCapture(1) に変更すること。
        """
        self.cap: cv2.VideoCapture = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.captured_img: np.ndarray | None = None
        if not self.cap.isOpened():
             print("エラー: カメラを開けませんでした。")

    def get_and_show_frame(self) -> np.ndarray | None:
        """カメラから1フレームを取得し、ターゲットマークを描画した加工画像を返す。"""
        ret, frame = self.cap.read()
        
        if not ret:
            self.captured_img = None
            return None 

        self.captured_img: np.ndarray = frame 

        img: np.ndarray = np.copy(frame)

        rows, cols, _ = img.shape
        center = (int(cols / 2), int(rows / 2))
        img = cv2.circle(img, center, 30, (0, 0, 255), 3)
        img = cv2.circle(img, center, 60, (0, 0, 255), 3)
        img = cv2.line(img, (center[0], center[1] - 80), (center[0], center[1] + 80), (0, 0, 255), 3)
        img = cv2.line(img, (center[0] - 80, center[1]), (center[0] + 80, center[1]), (0, 0, 255), 3)

        img = cv2.flip(img, flipCode=1)
        
        return img

    def get_img(self) -> np.ndarray | None:
        """最後にキャプチャされたオリジナル画像（加工前）を取得する。"""
        return self.captured_img
    
    def write_img(self, filepath: str = 'images/camera_capture.png') -> None:
        """キャプチャされた画像をファイルに保存する。"""
        if self.captured_img is None:
            raise ValueError("キャプチャ画像が存在しません。")

        cv2.imwrite(filepath, self.captured_img)

    def __del__(self) -> None:
        """終了処理。カメラリソースを解放し、OpenCVウィンドウを閉じる。"""
        if hasattr(self, 'cap') and self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()