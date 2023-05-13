# Main.py
import cv2
import numpy as np

# 이미지 불러오기, 절대 경로
image_0 = cv2.imread("/Users/wonjunjo/Desktop/vscode/opencv_work/MusicBoxSheet/plane.png")

# 이미지 이진화
def threshold(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    return image

# 1. 보표 영역 추출 및 그 외 노이즈 제거
def remove_nosie(image):
    image = threshold(image)    # 이미지 이진화
    mask = np.zeros(image.shape, np.uint8)  # 보표 영역만 추출하기 위해 마스크 생성
    cnt, labels, stats, centroids = cv2.connectedComponentsWithStats(image) # 이미지 레이블링
    for i in range(1, cnt): # 배경을 제외
        x, y, w, h, area = stats[i] # x, y 좌측 상단 좌표, area: 면적, 픽셀 수
        if w > image.shape[1] * 0.5:  # 보표 영역에만
            cv2.rectangle(mask, (x, y, w, h), (255, 0, 0), -1)  # 사각형 그리기
            
    masked_image = cv2.bitwise_and(image, mask)  # 보표 영역만 추출
    cv2.imshow('masked_image', masked_image)
    return masked_image
        
image_1 = remove_nosie(image_0)

# 이미지 띄우기
cv2.imshow('image', image_1)
cv2.waitKey(0)