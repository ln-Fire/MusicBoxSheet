import cv2
import numpy as np
import functions as fs
import modules

# 이미지 불러오기
image = cv2.imread("airplane.png")
image = cv2.resize(image, (800,681))

image_1 = modules.remove_noise(image)

cv2.imshow('image', image_1)
k = cv2.waitKey(0)
if k == 27:
    cv2.destroyAllWindows()
