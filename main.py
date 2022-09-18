import cv2 as cv
from collections import deque
# 한반도 데이터 불러옴
from area_detection import area_list
# 한글 출력용
from PIL import ImageFont, ImageDraw, Image

# 가시영상과 적외영상(변수명 바꾸기)
gasi_image = cv.imread('./resources/gasi_1220_1200.png', cv.IMREAD_GRAYSCALE)
dst = cv.resize(gasi_image, dsize=(0, 0), fx=0.5, fy=0.5, interpolation=cv.INTER_LINEAR)
gasi_image = dst
jukwae_image = cv.imread('./resources/jukwae_1220_1200.png', cv.IMREAD_GRAYSCALE)

print('---------------')
print(gasi_image.shape, jukwae_image.shape)
# 결과 출력용 한반도 지도
map = cv.imread('./resources/map.png')
maxValue = 255
thresh = 150
th, map = cv.threshold(map, thresh, maxValue, cv.THRESH_BINARY)
map = 255 - map

# 구름 이름
cloud_name_list = {'ww': '적란운', 'wg': '상층운', 'wb': '엷은 상층운', 'gw': '두꺼운 중층운',
                   'gg': '중층운', 'gb': '구름없음', 'bw': '하층운', 'bg': '안개',
                   'bb': '구름없음'}
cloud_color_list = {'ww': [255, 132, 58], 'wg': [160, 180, 23], 'wb': [97, 130, 124], 'gw': [105, 216, 173],
                    'gg': [235, 88, 0], 'gb': [223, 230, 247], 'bw': [40, 115, 110], 'bg': [205, 242, 228],
                    'bb': [255, 206, 176]}


# 구름의 종류 예측
def cloud(gasi_intensity, jukwae_intensity):
    cloud_info = ''
    if gasi_intensity > 214:
        cloud_info += 'w'
    elif gasi_intensity > 93.76:
        cloud_info += 'g'
    else:
        cloud_info += 'b'

    if jukwae_intensity > 163.96:
        cloud_info += 'w'
    elif jukwae_intensity > 64.12:
        cloud_info += 'g'
    else:
        cloud_info += 'b'

    cloud_name = cloud_name_list[cloud_info]
    cloud_color = cloud_color_list[cloud_info]

    return cloud_name, cloud_color


# 평균밝기 구하기
def mean_intensity(image):
    # cv.imshow('a', image)
    # cv.waitKey(0)
    pixel_area = area_list.get(key_area_name)
    intensity_sum = 0
    for x, y in pixel_area:
        print(x, y)
        intensity_sum += image[y + 290, x + 250]
    intensity = intensity_sum / len(pixel_area)
    print(intensity)
    return intensity


# main
text_y = 0
for key_area_name in area_list.keys():

    gasi_mean_intensity = mean_intensity(gasi_image)
    jukwae_mean_intensity = mean_intensity(jukwae_image)

    cloud_name, cloud_color = cloud(gasi_mean_intensity, jukwae_mean_intensity)

    # 시각화
    for x, y in area_list.get(key_area_name):
        map[x + 290, y + 250] = cloud_color
cv.imshow('cloud information', map)
cv.waitKey(0)
