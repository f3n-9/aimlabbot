import cv2
import time
import keyboard
import win32con
import win32api
import pyautogui
import pydirectinput
import numpy as np
import mss
import pygetwindow as gw

CUT_SIZE = 700

def show(img):
    cv2.imshow('Target Tracker', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        return False
    return True

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
            cv2.circle(img, (x, y), 10, (0, 255, 0), 2)  # 绘制检测到的目标
            return x, y

    # # 如果没有检测到目标，则绘制所有的轮廓
    # for c in cnts:
    #     cv2.drawContours(img, [c], -1, (0, 0, 255), 2)

    return None
# def checkCircle(img):
#     # 边缘检测
#     edged = cv2.Canny(img, 75, 200)
#     # 轮廓检测
#     contours = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     cnts = contours[0] if len(contours) == 2 else contours[1]
#     if cnts is None:
#         return None
#     for c in cnts:
#         x, y, w, h = cv2.boundingRect(c)
#         if np.abs(w - h) < 50 and cv2.contourArea(c) > 5000:
#             # 返回第一个坐标
#             return int(x + (w / 2)),int(y + (h / 2))
#     return None


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
    # return np.array(pyautogui.screenshot())
    sec = mss.mss()
    monitor = {
        "left": 0,
        "top": 0,
        "width": 2560,
        "height": 1440
    }
    return np.array(sec.grab(monitor))

def center_window(window_title):
    # 获取屏幕尺寸
    screen_width, screen_height = pyautogui.size()

    # 获取指定标题的窗口
    try:
        window = gw.getWindowsWithTitle(window_title)[0]
    except IndexError:
        print(f"No window found with the title: {window_title}")
        return

    # 获取窗口的尺寸
    window_width = window.width
    window_height = window.height

    # 计算新的窗口位置，以使其居中
    new_left = (screen_width - window_width) // 2
    new_top = (screen_height - window_height) // 2

    # 移动窗口到新位置
    window.moveTo(new_left, new_top)
    print(f"Window '{window_title}' has been centered.")

def drawCircle(img, x, y):
    cv2.circle(img, (x, y), 10, (0, 255, 0), 10)
    return show(img)

if __name__ == '__main__':
    cv2.namedWindow('Target Tracker', cv2.WINDOW_AUTOSIZE)
    running = False
    center_window('aimlab_tb')
    while True:
        if keyboard.is_pressed('9'):
            running = not running
            time.sleep(0.5)  # 小延迟避免重复触发

        if running:
            start = time.time()
            img = catchScreen()
            temp = checkCircle(pre(img))
            if temp is None:
                if not show(pre(img)):  # 显示没有目标的图像
                    break
            else:
                x, y = temp
                if not drawCircle(pre(img), x, y):  # 显示有目标的图像
                    break
            h, w = img.shape[:2]
            autoClick(x, y, h, w)
            print(time.time() - start)
