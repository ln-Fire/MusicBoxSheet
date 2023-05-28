# Main.py
import cv2
import os
import numpy as np
import functions as fs
import modules

# 이미지 불러오기
resource_path = os.getcwd()
image_0 = cv2.imread(resource_path + "/test/test2.png")

# 1. 보표 영역 추출 및 그 외 노이즈 제거
image_1 = modules.remove_noise(image_0)
cv2.imwrite('result1.png', image_1)

# 2. 오선 제거
image_2, staves = modules.remove_staves(image_1)
cv2.imwrite('result2.png', image_2)

# 3. 악보 이미지 정규화
# standard의 값에 따라 가중치가 달라짐
image_3, staves = modules.normalization(image_2, staves, 10)
cv2.imwrite('result3.png', image_3)

# 4. 객체 검출 과정 
image_4, objects = modules.object_detection(image_3, staves)
cv2.imwrite('result4.png', image_4)

# 5. 객체 분석 과정
image_5, objects = modules.object_analysis(image_4, objects)
cv2.imwrite('result5.png', image_5)

# 6. 인식 과정
image_6, key, beats, pitches = modules.recognition(image_5, staves, objects)

# 이미지 띄우기
# cv2.imshow('image0', image_0)
#cv2.imshow('image1', image_1)
# cv2.imshow('image2', image_2)
print(staves)
#cv2.imshow('image3', image_3)
#cv2.imshow('image4', image_4)
print(objects)
#cv2.imshow('image5', image_5)
#cv2.imshow('image6', image_6)
print(pitches)   # 음정 반환
print(beats)    # 박자 반환
cv2.imwrite('result.png', image_6)

k = cv2.waitKey(0)
if k == 27:
    cv2.destroyAllWindows()