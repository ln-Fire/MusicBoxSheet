# modules.py
import cv2
import numpy as np
import functions as fs
import recognition_modules as rs


def remove_noise(image):
    # 이미지 이진화
    image = fs.threshold(image)
    # 보표 영역만 추출하기 위해 마스크 생성
    mask = np.zeros(image.shape, np.uint8)

    # 레이블링
    cnt, labels, stats, centroids = cv2.connectedComponentsWithStats(image)
    for i in range(1, cnt):
        x, y, w, h, area = stats[i]
        # 보표 영역에만
        if w > image.shape[1] * 0.625:
            # 사각형 그리기
            cv2.rectangle(mask, (x, y, w, h), (255, 0, 0), -1)

    # 보표 영역 추출
    masked_image = cv2.bitwise_and(image, mask)

    return masked_image


def remove_staves(image):
    height, width = image.shape
    # 오선의 좌표들이 저장될 리스트
    staves = []
    # 각 오선 간의 간격과 y좌표를 저장할 리스트
    staves_info = []

    for row in range(height):
        pixels = 0
        for col in range(width):
            # 한 행에 존재하는 흰색 픽셀의 개수를 셈
            pixels += (image[row][col] == 255)
        # 이미지 넓이의 50% 이상이라면
        if pixels >= width * 0.5:
            # 첫 오선이거나 이전에 검출된 오선과 다른 오선
            if len(staves) == 0 or abs(
                    staves[-1][0] + staves[-1][1] - row) > 1:
                # 오선 추가 [오선의 y 좌표][오선 높이]
                staves.append([row, 0])
            # 이전에 검출된 오선과 같은 오선
            else:
                # 높이 업데이트
                staves[-1][1] += 1

    for staff in range(len(staves)):
        # 오선의 최상단 y 좌표
        top_pixel = staves[staff][0]
        # 오선의 최하단 y 좌표 (오선의 최상단 y 좌표 + 오선 높이)
        bot_pixel = staves[staff][0] + staves[staff][1]
        for col in range(width):
            # 오선 위, 아래로 픽셀이 있는지 탐색
            if image[top_pixel -
                     1][col] == 0 and image[bot_pixel +
                                            1][col] == 0:
                for row in range(top_pixel, bot_pixel + 1):
                    # 오선을 지움
                    image[row][col] = 0

        if staff < len(staves) - 1:
            # 다음 오선의 최상단 y 좌표
            next_top_pixel = staves[staff + 1][0]
            # 현재 오선과 다음 오선 사이의 간격
            spacing = next_top_pixel - bot_pixel
            staves_info.append([spacing, top_pixel])

    print(staves_info)
    return image, [x[0] for x in staves]


def normalization(image, staves, standard):
    avg_distance = 0
    # 보표의 개수
    lines = int(len(staves) / 5)
    for line in range(lines):
        for staff in range(4):
            staff_above = staves[line * 5 + staff]
            staff_below = staves[line * 5 + staff + 1]
            # 오선의 간격을 누적해서 더해줌
            avg_distance += abs(staff_above - staff_below)

    # 오선 간의 평균 간격
    avg_distance /= len(staves) - lines
    # 이미지의 높이와 넓이
    height, width = image.shape
    # 기준으로 정한 오선 간격을 이용해 가중치를 구함
    weight = standard / avg_distance
    # 이미지의 넓이에 가중치를 곱해줌
    new_width = int(width * weight)
    # 이미지의 높이에 가중치를 곱해줌
    new_height = int(height * weight)

    # 이미지 리사이징
    image = cv2.resize(image, (new_width, new_height),
                       interpolation=cv2.INTER_LINEAR)
    # 이미지 이진화
    ret, image = cv2.threshold(
        image, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # 오선 좌표에도 가중치를 곱해줌
    staves = [x * weight for x in staves]

    return image, staves


def object_detection(image, staves):
    # 보표의 개수
    lines = int(len(staves) / 5)
    # 구성요소 정보가 저장될 리스트
    objects = []

    closing_image = fs.closing(image)
    # 모든 객체 검출하기
    cnt, labels, stats, centroids = cv2.connectedComponentsWithStats(
        closing_image)
    for i in range(1, cnt):
        (x, y, w, h, area) = stats[i]
        # 악보의 구성요소가 되기 위한 넓이, 높이 조건
        if w >= fs.weighted(5) and h >= fs.weighted(5):
            center = fs.get_center(y, h)
            for line in range(lines):
                # 위치 조건 (상단)
                area_top = staves[line * 5] - fs.weighted(20)
                # 위치 조건 (하단)
                area_bot = staves[(line + 1) * 5 - 1] + fs.weighted(20)
                if area_top <= center <= area_bot:
                    # 객체 리스트에 보표 번호와 객체의 정보(위치, 크기)를 추가
                    objects.append([line, (x, y, w, h, area)])

    # 보표 번호 → x 좌표 순으로 오름차순 정렬, 악보의 객체 순서대로 정렬된 결과
    objects.sort()

    return image, objects


def object_analysis(image, objects):
    for i, obj in enumerate(objects):
        stats = obj[1]
        (x, y, w, h, area) = stats
        # 객체 내의 모든 직선들을 검출함
        stems = fs.stem_detection(image, stats, 30)
        direction = None
        # 직선이 1개 이상 존재함
        if len(stems) > 0:
            # 직선이 나중에 발견되면
            if stems[0][0] - stats[0] >= fs.weighted(5):
                # 정 방향 음표
                direction = True
            # 직선이 일찍 발견되면
            else:
                # 역 방향 음표
                direction = False
        # 객체 리스트에 직선 리스트를 추가
        obj.append(stems)
        # 객체 리스트에 음표 방향을 추가
        obj.append(direction)

        cv2.rectangle(image, (x, y, w, h), (255, 0, 0), 1)
        fs.put_text(image, i, (x, y - fs.weighted(20)))

    return image, objects


def recognition(image, staves, objects):
    key = 0
    time_signature = False
    # 박자 리스트
    beats = []
    # 음이름 리스트
    pitches = []

    for i in range(0, len(objects) - 1):
        obj = objects[i]
        line = obj[0]
        stats = obj[1]
        stems = obj[2]
        direction = obj[3]
        (x, y, w, h, area) = stats
        staff = staves[line * 5: (line + 1) * 5]
        notes = rs.recognize_note(image, staff, stats, stems, direction)
        if len(notes[0]):
            for beat in notes[0]:
                beats.append(beat)
            for pitch in notes[1]:
                pitches.append(pitch)
        else:
            rest = rs.recognize_rest(image, staff, stats)
            if rest:
                beats.append(rest)
                pitches.append(0)
            else:
                whole_note, pitch = rs.recognize_whole_note(
                    image, staff, stats)
                if whole_note:
                    beats.append(whole_note)
                    pitches.append(pitch)

        cv2.rectangle(image, (x, y, w, h), (255, 0, 0), 1)
        fs.put_text(image, i, (x, y - fs.weighted(20)))

    return image, beats, pitches