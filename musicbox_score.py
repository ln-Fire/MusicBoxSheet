import cv2
import numpy as np

def musicbox_score(pitches, beats):
    all_beat = 0  # 모든 박자 수를 셈

    for i in range(len(beats)):
        all_beat += beats[i]
    all_beat //= 8  # 4분음표를 한박(1)로 하려면 8로 나눠줄 필요가 있음

    make_red = [7, 19, 27]  # 빨간줄이 들어있어야되는 배열
    musicbox_score = np.zeros((3500, (all_beat * 100) + 3200, 3), dtype="uint8") + 255
    # 앞뒤 여유공간 600씩 1200에 박자수 만큼 악보의 x길이 결정

    score_size = (all_beat * 100) + 2600  # 악보의 size만큼 가로줄의 길이 및 세로줄 개수 결정

    for i in range(0, 30):  # 가로줄 생성. 도는 빨간줄 처리
        if i in make_red:
            cv2.line(musicbox_score, (600, (i * 100) + 300), (score_size, (i * 100) + 300), (0, 0, 255), 3)
        else:
            cv2.line(musicbox_score, (600, (i * 100) + 300), (score_size, (i * 100) + 300), (0, 0, 0), 3)

    make_beatline = 800
    make_beatsubline = 700
    cv2.line(musicbox_score, (600, 300), (600, 3200), (0, 0, 0), 3)  # 시작 세로선

    for i in range(0, (all_beat // 2) + 10):  # 세로줄 생성. 도는 빨간줄 처리
        subline_helper = 375
        cv2.line(musicbox_score, (make_beatsubline, 300), (make_beatsubline, 325), (0, 0, 0), 2)  # 맨 위 보조선
        for i in range(1, 29):  # 중간 보조선들 생성
            if i in make_red:
                cv2.line(musicbox_score, (make_beatsubline, subline_helper), (make_beatsubline, subline_helper + 50), (0, 0, 255), 2)
                subline_helper += 100
            else:
                cv2.line(musicbox_score, (make_beatsubline, subline_helper), (make_beatsubline, subline_helper + 50), (0, 0, 0), 2)
                subline_helper += 100
        cv2.line(musicbox_score, (make_beatsubline, 3200), (make_beatsubline, 3175), (0, 0, 0), 2)  # 맨 아래 보조선

        cv2.line(musicbox_score, (make_beatline, 300), (make_beatline, 3200), (0, 0, 0), 3)  # 메인 세로선
        make_beatline += 200
        make_beatsubline += 200

    x = 800
    y = 300

    for i in range(len(pitches)):  # for i in range(len(beats)): 해도 size는 같으므로 상관 없음
        if pitches[i] > 0:
            y += (30 - pitches[i]) * 100
            cv2.circle(musicbox_score, (x, y), 25, (0, 0, 0), -1)
            y = 300
        x += beats[i] * 25

    return musicbox_score