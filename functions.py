# functions.py
import cv2
import numpy as np

# 이미지 이진화
def threshold(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, image = cv2.threshold(
        image, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
    return image

# 정규화 가중치 설정
def weighted(value):
    standard = 20
    return int(value * (standard / 10))

# closing 연산
def closing(image):
    kernel = np.ones((weighted(5), weighted(5)), np.uint8)
    image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
    return image

# 출력 이미지에 글씨 작성
def put_text(image, text, loc):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(image, str(text), loc, font, 0.6, (255, 0, 0), 2)

# 중심 반환
def get_center(y, h):
    return (y + y + h) / 2


VERTICAL = True
HORIZONTAL = False


def get_line(image, axis, axis_value, start, end, length):
    if axis:
        # 수직 탐색
        points = [(i, axis_value) for i in range(start, end)]
    else:
        # 수평 탐색
        points = [(axis_value, i) for i in range(start, end)]
    pixels = 0
    for i in range(len(points)):
        (y, x) = points[i]
        # 흰색 픽셀의 개수를 셈
        pixels += (image[y][x] == 255)
        # 다음 탐색할 지점
        next_point = image[y + 1][x] if axis else image[y][x + 1]
        # 선이 끊기거나 마지막 탐색임
        if next_point == 0 or i == len(points) - 1:
            if pixels >= weighted(length):
                # 찾는 길이의 직선을 찾았으므로 탐색을 중지함
                break
            else:
                # 찾는 길이에 도달하기 전에 선이 끊김 (남은 범위 다시 탐색)
                pixels = 0
    return y if axis else x, pixels

# 음표의 기둥 탐지
def stem_detection(image, stats, length):
    (x, y, w, h, area) = stats
    # 기둥 정보 (x, y, w, h)
    stems = []
    for col in range(x, x + w):
        end, pixels = get_line(image, VERTICAL, col, y, y + h, length)
        if pixels:
            if len(stems) == 0 or abs(stems[-1][0] + stems[-1][2] - col) >= 1:
                (x, y, w, h) = col, end - pixels + 1, 1, pixels
                stems.append([x, y, w, h])
            else:
                stems[-1][2] += 1
    return stems

# 점 픽셀의 개수를 셈
def count_rect_pixels(image, rect):
    x, y, w, h = rect
    pixels = 0
    for row in range(y, y + h):
        for col in range(x, x + w):
            if image[row][col] == 255:
                pixels += 1
    return pixels

# 부분 픽셀의 개수를 셈
def count_pixels_part(image, area_top, area_bot, area_col):
    cnt = 0
    flag = False
    for row in range(area_top, area_bot):
        if not flag and image[row][area_col] == 255:
            flag = True
            cnt += 1
        elif flag and image[row][area_col] == 0:
            flag = False
    return cnt