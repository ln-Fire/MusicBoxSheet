# Main.py
import cv2
import os
import modules
import musicbox_score as ms

# 이미지 불러오기
resource_path = os.getcwd()
image_0 = cv2.imread(resource_path + '/test/soccer.png')
cv2.imshow("input image", image_0)
cv2.imwrite("0. 디지털 악보.png", image_0)

# 1. 노이즈 제거 및 보표 영역 추출
image_1 = modules.remove_noise(image_0)
cv2.imshow("remove noise", image_1)
cv2.imwrite("1. 노이즈 제거 및 보표 영역 추출.png", image_1)

# 2. 오선 제거
image_2, staves = modules.remove_staves(image_1)
cv2.imshow("remove staves", image_2)
cv2.imwrite("2. 오선 제거.png", image_2)
print()
print(staves)
print()

# 3. 악보 이미지 정규화
image_3, staves = modules.normalization(image_2, staves, 20)
cv2.imshow("normalization", image_3)
cv2.imwrite("3. 악보 이미지 정규화.png", image_3)
print(staves)
print()

# 4. 객체 검출
image_4, objects = modules.object_detection(image_3, staves)
cv2.imshow("object detection", image_4)
cv2.imwrite("4. 악보 안의 객체 검출.png", image_4)
print(objects)
print()

# 5. 객체 분석
image_5, objects = modules.object_analysis(image_4, objects)
cv2.imshow("object analysis", image_5)
cv2.imwrite("5. 악보 안의 객체 분석.png", image_5)
print(objects)
print()

# 6. 객체 인식
image_6, beats, pitches = modules.recognition(image_5, staves, objects)
cv2.imshow("object recognition", image_6)
cv2.imwrite("6. 악보 안의 객체 인식.png", image_6)

print()
# 박자
print(beats)
print()
# 음정
print(pitches)
print()

# 슛돌이
beats_soccer = [8, 8, 8, 8, 4, 4, 4, 4, 16, 4, 4, 4, 4, 8, 8, 4, 4, 4, 4, 8, 8, 8, 8, 8, 8, 4, 4, 4, 4, 16, 8, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 8, 8, 8, 8, 8, 8, 8, 4, 4, 4, 4, 8, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 8, 8, 8, 8, 8, 8, 8, 4, 4, 4, 4, 8, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 8, 8, 8]
pitches_soccer = [11, 0, 11, 11, 13, 13, 12, 11, 0, 13, 12, 11, 12, 13, 11, 12, 13, 14, 15, 14, 0, 11, 0, 11, 11, 13, 13, 12, 11, 0, 10, 10, 10, 11, 11, 11, 13, 11, 12, 13, 14, 15, 0, 8, 8, 8, 0, 8, 8, 8, 8, 8, 8, 10, 10, 10, 9, 8, 8, 8, 8, 7, 8, 9, 8, 7, 0, 8, 8, 8, 0, 8, 8, 8, 8, 8, 8, 10, 10, 10, 9, 8, 8, 8, 8, 7, 11, 0, 8, 0]

# 작은 별
beats_little_star = [8, 8, 8, 8, 8, 8, 16, 8, 8, 8, 8, 8, 8, 16, 8, 8, 8, 8, 8, 8, 16, 8, 8, 8, 8, 8, 8, 16, 8, 8, 8, 8, 8, 8, 16, 8, 8, 8, 8, 8, 8, 16]
pitches_little_star = [15, 15, 11, 11, 10, 10, 11, 12, 12, 13, 13, 14, 14, 15, 11, 11, 12, 12, 13, 13, 14, 11, 11, 12, 12, 13, 13, 14, 15, 15, 11, 11, 10, 10, 11, 12, 12, 13, 13, 14, 14, 15]

# 오르골 악보 생성
music_box_sheet = ms.musicbox_score(beats_soccer, pitches_soccer)
music_box_sheet = ms.musicbox_score(pitches_little_star, pitches_little_star)
music_box_sheet = ms.musicbox_score(pitches, beats)
cv2.imshow("musicbox", music_box_sheet)
cv2.imwrite("7. 오르골 악보 생성.png", music_box_sheet)

k = cv2.waitKey(0)
if k == 27:
    cv2.destroyAllWindows()