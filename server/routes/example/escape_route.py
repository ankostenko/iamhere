"""
Консольное приложение для распознование пути
"""
import matplotlib.image as mpimg
# from PIL import Image
import numpy
import matplotlib.pyplot as plt
import cv2

from datetime import datetime

from server.routes.pixel import Pixel
from server.routes.identify_obstacles import IdentifyObstacles
from server.routes.complexity_way import ComplexityWay
from server.routes.searcher_way import SearcherWay
from server.routes.image_compression import DominateColor
from server.routes.image_compression import ImageCompression
from server.routes.way_finder import WayFinder
from server.routes.searcher_coordinate import SearcherCoordinate
from server.routes.door_search import DoorSearch


if __name__ == '__main__':
    # img = Image.open('floor_2.png').resize((100, 100))
    # pix = numpy.asarray(img)
    # for row in pix:
    #     for pixel in row:
    #         print(pixel, end='')
    #     print('')
    file_name = 'floor_2.png'
    start_time = datetime.now()
    print('Открытие файла', start_time)
    # img = mpimg.imread('simple2.png')  # simple1.png stinkbug.png
    img = mpimg.imread(file_name)  # simple1.png stinkbug.png
    image_compression = DominateColor(img)
    dominate_color = image_compression.get()
    # compress_img = image_compression.compress(img, )
    z = ImageCompression(img, dominate_color)
    compress_img = z.compress()
    print('Чтение данных из файла')
    print('Нахождение препятствий и свободного пространства')
    identify_obstacles = IdentifyObstacles(compress_img)
    identify_obstacles.find_obstacle_and_free_space()
    # identify_obstacles.print_surface_type()
    identify_obstacles.save_file_surface_type(img)

    imgDoor = cv2.imread(file_name)
    door = DoorSearch(imgDoor)
    door.Search(compress_img)

    print('Нахождение сложности поверхности чем дальше от стены тем проще.')
    complexity_way = ComplexityWay(compress_img)
    complexity_way.find_complexity_way()
    # complexity_way.print_complexity_way()
    complexity_way.save_file_complexity_way(img)
    # complexity_way.save_complexity_way_to_json(file_name)
    # complexity_way.load_complexity_way_from_json(file_name)

    print('Нахождение пути.')
    searcher_way = SearcherWay(compress_img)
    # fined_way = searcher_way.find_way((10, 0), (10, 10))
    fined_way = searcher_way.find_way(
        SearcherCoordinate((560, 540), compress_img).get_coordinate(),
        SearcherCoordinate((560, 630), compress_img).get_coordinate()
    )
    # fined_way = searcher_way.find_way((757, 819), (1501, 1447))
    # fined_way = searcher_way.find_way((819, 757), (1447, 1501))
    # fined_way = searcher_way.find_way((578, 430), (824, 1041))
    # searcher_way.print_way(fined_way)
    searcher_way.save_file_way(fined_way, img)
    print('find_way_coordinate:', searcher_way.find_way_coordinate(fined_way))

    print('--- Итоговый класс для вычисление пути. ---')
    finder = WayFinder('floor_2.png')
    print('find_way:', finder.find_way(560, 540, 560, 630))
    # print('find_way:', finder.find_way(coor_row, coor_col, 824, 1041))
    # print('find_way:', finder.find_way(coordinate, 1501, 1447))
