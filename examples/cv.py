import cv2

# 读取图像
image = cv2.imread('a.png')

# 显示图像
cv2.imshow('Image', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
