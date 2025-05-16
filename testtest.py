import pydirectinput
import pyautogui
import time
import win32api
import win32con

while True:
    currentX, currentY = pydirectinput.position()
    print(currentX,currentY)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 10, 10)
    time.sleep(0.001)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.001)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(0.1)