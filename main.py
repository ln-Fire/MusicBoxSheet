# Main.py
import cv2
import os
import numpy as np
import functions as fs
import modules
import musicbox_score as ms

# 이미지 불러오기
resource_path = os.getcwd()
image_0 = cv2.imread(resource_path + "/test/soccer.png")

# 1. 보표 영역 추출 및 그 외 노이즈 제거
image_1 = modules.remove_noise(image_0)

# 2. 오선 제거
image_2, staves = modules.remove_staves(image_1)

# 3. 악보 이미지 정규화
image_3, staves = modules.normalization(image_2, staves, 20)

# 4. 객체 검출 과정 
image_4, objects = modules.object_detection(image_3, staves)

# 5. 객체 분석 과정
image_5, objects = modules.object_analysis(image_4, objects)

# 6. 인식 과정
image_6, key, beats, pitches = modules.recognition(image_5, staves, objects)

# 오르골 악보 만들기
music_box_sheet = ms.musicbox_score(pitches, beats)

# 이미지 띄우기
# cv2.imshow('image0', image_0)
# cv2.imshow('image1', image_1)
# cv2.imshow('image2', image_2)
cv2.imshow('image3', image_3)
cv2.imshow('image4', image_4)
print(objects)
cv2.imshow('image5', image_5)
cv2.imshow('image6', image_6)
cv2.imwrite('result.png', image_6)
print(pitches)   # 음정 반환
print()
print(beats)    # 박자 반환
cv2.imwrite('result.png', image_5)
cv2.imwrite('musicboxresult.png', music_box_sheet)

k = cv2.waitKey(0)
if k == 27:
    cv2.destroyAllWindows()