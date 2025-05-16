import cv2
import time
import keyboard
import win32con
import win32api
import pydirectinput
import numpy as np
import mss


CUT_SIZE = 700


def pre(img):
    h, w = img.shape[:2]
    img = img[int(h/2-CUT_SIZE):int(h/2+CUT_SIZE), int(w/2-CUT_SIZE):int(w/2+CUT_SIZE)]
    return img


def checkCircle(img):
    # 降低图像分辨率
    img_small = cv2.resize(img, (0, 0), fx=1/4, fy=1/4)

    # 边缘检测
    edged = cv2.Canny(img_small, 75, 200)
    # 轮廓检测
    contours = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = contours[0] if len(contours) == 2 else contours[1]
    if cnts is None:
        return None
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        if np.abs(w - h) < 10 and cv2.contourArea(c) > 350:
            # 返回原图像坐标
            x, y = int((x + w / 2) * 4), int((y + h / 2) * 4)
            return x, y
    return None

def autoClick(x, y, h, w):
    x = int(x + w / 2 - CUT_SIZE)
    y = int(y + h / 2 - CUT_SIZE)
    currentX, currentY = pydirectinput.position()
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x - currentX, y - currentY)
    time.sleep(0.001)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.001)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def catchScreen():
    with mss.mss() as sct:
        monitor = {
            "left": 0,
            "top": 0,
            "width": 2560,
            "height": 1440
        }
        sct_img = sct.grab(monitor)
        return np.array(sct_img)


if __name__ == '__main__':
    running = False


    while True:
        if keyboard.is_pressed('9'):
            running = not running
            time.sleep(0.5)  # 小延迟避免重复触发

        if running:
            start = time.time()
            img = catchScreen()
            temp = checkCircle(pre(img))
            if temp is None:
                break
            else:
                x, y = temp
            h, w = img.shape[:2]
            autoClick(x, y, h, w)
            print(time.time() - start)
