import cv2
import numpy as np


def musicbox_score(pitches, beats):
    # 모든 박자 수를 셈
    all_beat = 0

    for i in range(len(beats)):
        all_beat += beats[i]
    # 4분음표를 한박(1)로 하려면 8로 나눠줄 필요가 있음
    all_beat //= 8

    # 앞뒤 여유공간 64 * 6 = 384씩 총 768에 박자수 만큼 악보의 x길이 결정, 악보 위는 64*3 = 192 아래도
    # 동일하게, 음표의 한 칸 넓이인 64*14해서 64*(14+3+3)인 1280
    musicbox_score = np.zeros((1280, (all_beat * 128) + 768, 3), dtype="uint8") + 255

    # 악보의 size만큼 가로줄의 길이 및 세로줄 개수 결정
    score_size = (all_beat * 128)

    # 가로줄 생성. 도는 빨간줄 처리
    for i in range(0, 15):
        if i == 7:
            cv2.line(musicbox_score, (384, (i * 64) + 192),
                     (score_size + 384, (i * 64) + 192), (0, 0, 255), 3)
        else:
            cv2.line(musicbox_score, (384, (i * 64) + 192),
                     (score_size + 384, (i * 64) + 192), (0, 0, 0), 3)

    make_beatline = 512
    make_beatsubline = 448
    # 시작 세로선
    cv2.line(musicbox_score, (384, 192), (384, 1088), (0, 0, 0), 3)

    # 세로줄 생성. 도는 빨간줄 처리
    for i in range(0, all_beat):
        subline_helper = 256
        # 맨 위 보조선
        cv2.line(musicbox_score, (make_beatsubline, 192),
                 (make_beatsubline, 192 + 16), (0, 0, 0), 2)
        # 중간 보조선들 생성
        for i in range(1, 14):
            if i == 7:
                cv2.line(musicbox_score, (make_beatsubline, subline_helper - 16),
                         (make_beatsubline, subline_helper + 16), (0, 0, 255), 2)
                subline_helper += 64
            else:
                cv2.line(musicbox_score, (make_beatsubline, subline_helper - 16),
                         (make_beatsubline, subline_helper + 16), (0, 0, 0), 2)
                subline_helper += 64
        # 맨 아래 보조선
        cv2.line(musicbox_score, (make_beatsubline, 1280 - 192),
                 (make_beatsubline, 1280 - 192 - 16), (0, 0, 0), 2)

        # 메인 세로선
        cv2.line(musicbox_score, (make_beatline, 192),
                 (make_beatline, 1088), (0, 0, 0), 3)
        make_beatline += 128
        make_beatsubline += 128

    x = 384
    y = 128
    for i in range(len(pitches)):
        if pitches[i] is None:
            continue
        if pitches[i] > 0:
            y += pitches[i] * 64
            cv2.circle(musicbox_score, (x, y), 20, (0, 0, 0), -1)
            y = 128

        x += beats[i] * 16

    return musicbox_score