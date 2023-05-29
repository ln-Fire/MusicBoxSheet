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
cv2.imshow('input image', image_0)
cv2.imwrite('0. 디지털 악보.png', image_0)

# 1. 노이즈 제거 및 보표 영역 추출
image_1 = modules.remove_noise(image_0)
cv2.imshow('remove noise', image_1)
cv2.imwrite('1. 노이즈 제거 및 보표 영역 추출.png', image_1)

# 2. 오선 제거
image_2, staves = modules.remove_staves(image_1)
cv2.imshow('remove staves', image_2)
cv2.imwrite('2. 오선 제거.png', image_2)
print()
print(staves)
print()

# 3. 악보 이미지 정규화
image_3, staves = modules.normalization(image_2, staves, 20)
cv2.imshow('normalization', image_3)
cv2.imwrite('3. 악보 이미지 정규화.png', image_3)
print(staves)
print()

# 4. 객체 검출
image_4, objects = modules.object_detection(image_3, staves)
cv2.imshow('object detection', image_4)
cv2.imwrite('4. 악보 안의 객체 검출.png', image_4)
print(objects)
print()

# 5. 객체 분석
image_5, objects = modules.object_analysis(image_4, objects)
cv2.imshow('object analysis', image_5)
cv2.imwrite('5. 악보 안의 객체 분석.png', image_5)
print(objects)
print()

# 6. 객체 인식
image_6, key, beats, pitches = modules.recognition(image_5, staves, objects)
cv2.imshow('object recognition', image_6)
cv2.imwrite('6. 악보 안의 객체 인식.png', image_6)
print(key)  # 조표
print()
print(beats)    # 박자
print()
print(pitches)  # 음정
print()

# 오르골 악보 생성
music_box_sheet = ms.musicbox_score(pitches, beats)
cv2.imshow('musicbox', music_box_sheet)
cv2.imwrite('7. 오르골 악보 생성.png', music_box_sheet)

k = cv2.waitKey(0)
if k == 27:
    cv2.destroyAllWindows()