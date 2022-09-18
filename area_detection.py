import cv2 as cv
from collections import deque

# 심야시간대의 가시영상 불러옴
original_image = cv.imread('./resources/gasimap.png')
# 전처리(한반도 영역 추출 > Grayscale변환 > 문턱값을 적용한 이진화)
south_korea = original_image[290:500, 250:500].copy()
gray_south_korea = cv.cvtColor(south_korea, cv.COLOR_BGR2GRAY)
maxValue = 255
thresh = 150
th, binary_south_korea = cv.threshold(gray_south_korea, thresh, maxValue, cv.THRESH_BINARY)

# 이진화된 한반도이미지의 가로X세로 크기를 가져옴(고정값)
width, height = binary_south_korea.shape

visited = [[False for j in range(height)] for i in range(width)]
area_info = {(78, 40): '서울특별시', (89, 43): '경기도', (116, 31): '강원도', (127, 79): '경상북도', (125, 101): '대구광역시',
             (145, 111): '울산광역시', (116, 118): '경상남도', (99, 66): '충청북도', (74, 78): '충청남도', (87, 79): '세종특별자치시',
             (90, 84): '대전광역시', (83, 107): '전라북도', (79, 138): '전라남도', (142, 123): '부산광역시', (74, 128): '광주광역시',
             (189, 39): '경상북도 울릉군', (66, 192): '제주특별자치도'}
area_list = {}


def bfs(binary_south_korea, start, visited):
    global area_info
    area = []
    area_name = 'None'
    queue = deque([start])
    area.append(start)
    visited[start[0]][start[1]] = True
    while queue:
        v = queue.popleft()
        # 상하좌우 검색
        for y, x in [[v[0] - 1, v[1]], [v[0] + 1, v[1]], [v[0], v[1] - 1], [v[0], v[1] + 1]]:
            # 판에서 안벗어나는지 확인
            if 0 <= y and y < width and 0 <= x and x < height:
                if not visited[y][x]:
                    # 같은 종류의 타일인지 확인
                    if binary_south_korea[v[0], v[1]] == binary_south_korea[y, x]:
                        visited[y][x] = True
                        area.append([y, x])
                        queue.append([y, x])
                        if (x, y) in area_info:
                            area_name = area_info[(x, y)]
                            area_list[area_name] = area
    return area_name, area


check_detected_area = 0
for i in range(0, height):
    for j in range(0, width):
        if binary_south_korea[i, j] == 0 and visited[i][j] == False:
            start = [i, j]
            area_name, area = bfs(binary_south_korea, start, visited)
            if area_name != 'None':
                check_detected_area += 1
                # 출력부
                dst = south_korea.copy()
                for y, x in area:
                    dst[y, x] = [255, 255, 255]
                cv.imshow('dst', dst)
                cv.waitKey(0)
                print(area_name, ':', len(area))
        if check_detected_area == 17:
            break
    if check_detected_area == 17:
        break
print(area_list)
