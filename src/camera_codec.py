import numpy as np
import cv2
from module.camera_image_capture import MyVideoCapture

# =========================================================================
# GUIボタンとマウスイベント処理のための設定と関数
# =========================================================================

# グローバル変数: 撮影がトリガーされたかを判定
SHOOT_TRIGGERED: bool = False
WINDOW_NAME: str = 'Camera View' 

# ボタンの座標設定 (右下に配置)
BUTTON_X_START: int = 500
BUTTON_Y_START: int = 400
BUTTON_WIDTH: int = 120
BUTTON_HEIGHT: int = 50
BUTTON_COLOR_IDLE = (100, 100, 100) # 灰色
BUTTON_COLOR_TEXT = (255, 255, 255) # 白

def mouse_callback(event: int, x: int, y: int, flags: int, param: any):
    """マウスイベントを処理するコールバック関数。"""
    global SHOOT_TRIGGERED
    x_end = BUTTON_X_START + BUTTON_WIDTH
    y_end = BUTTON_Y_START + BUTTON_HEIGHT

    if event == cv2.EVENT_LBUTTONDOWN:
        if BUTTON_X_START <= x <= x_end and BUTTON_Y_START <= y <= y_end:
            SHOOT_TRIGGERED = True 

def draw_button(img: np.ndarray):
    """画像に「SHOOT」ボタンを描画する。 (日本語フォントの問題回避のため英語表記)"""
    
    cv2.rectangle(
        img, 
        (BUTTON_X_START, BUTTON_Y_START), 
        (BUTTON_X_START + BUTTON_WIDTH, BUTTON_Y_START + BUTTON_HEIGHT), 
        BUTTON_COLOR_IDLE, 
        -1 
    )
    
    
    text = "SHOOT"  # "撮影"だと????となってしまうため"SHOOT"
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.8  # サイズを調整
    thickness = 2
    
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    text_x = BUTTON_X_START + (BUTTON_WIDTH - text_size[0]) // 2
    text_y = BUTTON_Y_START + (BUTTON_HEIGHT + text_size[1]) // 2
    
    cv2.putText(
        img, 
        text, 
        (text_x, text_y), 
        font, 
        font_scale, 
        BUTTON_COLOR_TEXT, 
        thickness, 
        cv2.LINE_AA
    )


def camera_codec() -> np.ndarray | None:
    """撮影ウィンドウを開き、GUIボタンで撮影をトリガーするメイン関数。"""
    global SHOOT_TRIGGERED
    
    app = MyVideoCapture()
    captured_frame = None
    SHOOT_TRIGGERED = False 

    cv2.namedWindow(WINDOW_NAME)
    cv2.setMouseCallback(WINDOW_NAME, mouse_callback)
    
    if not app.cap.isOpened():
        app.__del__()
        return None

    try:
        while True:
            processed_img = app.get_and_show_frame()
            
            if processed_img is None:
                break 
                
            draw_button(processed_img)
            cv2.imshow(WINDOW_NAME, processed_img)
            
            key = cv2.waitKey(1) & 0xFF
            
            if SHOOT_TRIGGERED: 
                captured_frame = app.get_img() 
                break
                
            if key == 27: 
                break
                
    finally:
        app.__del__() 
        
    return captured_frame