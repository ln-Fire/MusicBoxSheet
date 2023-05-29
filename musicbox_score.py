import cv2
import numpy as np

all_beat = 100  # 모든 박자 수를 셈

make_red = [7, 19, 27]  # 빨간줄이 들어있어야되는 배열
musicbox_score = np.zeros((7000, (all_beat * 200) + 2400, 3), dtype="uint8") + 255
# 앞뒤 여유공간 600씩 1200에 박자수 만큼 악보의 x길이 결정

score_size = (all_beat * 200) + 1200  # 악보의 size만큼 가로줄의 길이 및 세로줄 개수 결정

for i in range(0, 30):  # 가로줄 생성. 도는 빨간줄 처리
    if i in make_red:
        cv2.line(musicbox_score, (1200, (i * 200) + 600), (score_size, (i * 200) + 600), (0, 0, 255), 6)
    else:
        cv2.line(musicbox_score, (1200, (i * 200) + 600), (score_size, (i * 200) + 600), (0, 0, 0), 6)

make_beatline = 1600
make_beatsubline = 1400
cv2.line(musicbox_score, (1200, 600), (1200, 6400), (0, 0, 0), 6)  # 시작 세로선

for i in range(0, (all_beat // 2)):  # 세로줄 생성. 도는 빨간줄 처리
    subline_helper = 750
    cv2.line(musicbox_score, (make_beatsubline, 600), (make_beatsubline, 650), (0, 0, 0), 4)  # 맨 위 보조선
    for i in range(1, 29):  # 중간 보조선들 생성
        if i in make_red:
            cv2.line(musicbox_score, (make_beatsubline, subline_helper), (make_beatsubline, subline_helper + 100), (0, 0, 255), 4)
            subline_helper += 200
        else:
            cv2.line(musicbox_score, (make_beatsubline, subline_helper), (make_beatsubline, subline_helper + 100), (0, 0, 0), 4)
            subline_helper += 200
    cv2.line(musicbox_score, (make_beatsubline, 6400), (make_beatsubline, 6350), (0, 0, 0), 4)  # 맨 아래 보조선

    cv2.line(musicbox_score, (make_beatline, 600), (make_beatline, 6400), (0, 0, 0), 6)  # 메인 세로선
    make_beatline += 400
    make_beatsubline += 400

x = 1200
y = 600
for i in range(0, 3):
    for j in range(0, 30):
        cv2.circle(musicbox_score, (x, y), 60, (0, 0, 0), -1)
        y += 200
        x += 200
    y = 600

cv2.imshow('musicbox_score', musicbox_score)
cv2.imwrite('musicbox_score.png', musicbox_score)
if cv2.waitKey(0) == 27:
    cv2.destroyAllWindows()