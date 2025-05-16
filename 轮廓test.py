import cv2

CUT_SIZE = 300

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
    # 边缘检测
    edged = cv2.Canny(img, 75, 200)
    show(edged)
    return None


if __name__ == '__main__':
    img = cv2.imread("4.png")
    img = pre(img)
    checkCircle(img)