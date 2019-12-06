import itertools
import matplotlib.image as mpimg
import numpy as np

from server.routes.surface_type import SurfaceType
from server.routes.surface import Surface
from server.routes.helper_debug.calculation_time import calculation_time
from server.routes.helper_debug.path_logs import PathLogs


class IdentifyObstacles:
    """
    Нахождение препятствий и свободного пространства
    """
    def __init__(self, pixels):
        """
        Конструктор

        Args:
            pixels (numpy.ndarray): поле пикселей numpy.ndarray<numpy.ndarray<pictures.pixel.Pixel>>
        """
        self.__pixels = pixels
        # разница между цветами по свободного пространства
        self.__free_space_depth = 0.3

    @calculation_time
    def find_obstacle_and_free_space(self):
        """
        Поиск препятствий и свободного пространоства
        """
        pass

    @calculation_time
    def print_surface_type(self):
        """
        Печать типа опдстилающей поверхности
        """
        for row_result in self.__pixels:
            for pixel in row_result:
                surface_type = pixel.surface.surface_type
                print(surface_type.name[0:1] if surface_type != SurfaceType.FREE_SPACE else ' ', sep='', end='')
            print()

    @calculation_time
    def save_file_surface_type(self, source_img):
        """
        сохранение файла картинки
        цвет препятствий - Черный
        сложность прохождение пространосва - оттенки зеленого

        Args:
            source_img (numpy.ndarray): исходное изображение
        """
        for row_source, row_pixel in zip(source_img, self.__pixels):
            for source_pixel, pixel in zip(row_source, row_pixel):
                color = 1.0 - pixel.surface.surface_type.difficulty_overcome
                source_pixel[0] = color
                source_pixel[1] = color
                source_pixel[2] = color
        path = PathLogs.get_path_obstacles_file()
        mpimg.imsave(path, source_img)  # , format="'png'"
