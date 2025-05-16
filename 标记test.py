import cv2
import numpy as np

CUT_SIZE = 700

def show(img):
    cv2.imshow('name', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def pre(img):
    h, w = img.shape[:2]
    # 裁剪
    img = img[int(h/2-CUT_SIZE):int(h/2+CUT_SIZE),int(w/2-CUT_SIZE):int(w/2+CUT_SIZE)]
    return img

def checkCircle(img):
    # 降低图像分辨率
    img_small = cv2.resize(img, (0, 0), fx=1 / 4, fy=1 / 4)
    print("开始边缘检测")
    edged = cv2.Canny(img_small, 75, 200)

    print("开始轮廓检测")
    contours = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = contours[0] if len(contours) == 2 else contours[1]

    if len(cnts) == 0:
        print("未找到轮廓")
        return None, None

    print(f"找到 {len(cnts)} 个轮廓")
    cv2.drawContours(img_small, cnts, -1, (0, 0, 255), 5)

    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        area = cv2.contourArea(c)
        print(f"轮廓尺寸：宽度={w}, 高度={h}, 面积={area}")
        if np.abs(w - h) < 10 and area > 120:
            print("找到一个圆形轮廓")
            return img_small, (int(x + w / 2), int(y + h / 2))

    print("没有找到符合条件的圆形轮廓")
    return img_small, None

def drawCircle(img, x, y):
    cv2.circle(img, (x, y), 10, (0, 255, 0), 10)
    show(img)



if __name__ == '__main__':
    img = cv2.imread('hard2.png')
    if img is None:
        print("图像文件无法读取")
    else:
        img = pre(img)
        img, circle_center = checkCircle(img)
        if circle_center:
            drawCircle(img, *circle_center)  # 显示图像并画出圆心
        else:
            show(img)  # 如果没有找到圆形，仍然显示图像