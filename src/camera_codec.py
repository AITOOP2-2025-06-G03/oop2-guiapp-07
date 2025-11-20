import numpy as np
import cv2
from module.camera_image_capture import MyVideoCapture

def camera_codec():

    # カメラキャプチャ実行
    app = MyVideoCapture()
    app.run()

    # 画像をローカル変数に保存
    google_img : cv2.Mat = cv2.imread('images/google.png')
    capture_img : cv2.Mat = app.get_img()

    g_hight, g_width, g_channel = google_img.shape
    c_hight, c_width, c_channel = capture_img.shape
    print(google_img.shape)
    print(capture_img.shape)

    for x in range(g_width):
        for y in range(g_hight):
            g, b, r = google_img[y, x]
            # もし白色(255,255,255)だったら置き換える
            if (b, g, r) == (255, 255, 255):
                pass
                x1, y1 = x, y
                if x1 >= c_width:
                    x1 -= c_width
                if y1 >= c_hight:
                    y1 -= c_hight
                google_img[y, x] = capture_img[y1, x1]

    # 書き込み処理
    cv2.imwrite('output_images/result.png', google_img)

