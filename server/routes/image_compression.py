import numpy as np
import random
from server.routes.surface import Surface
from server.routes.surface_type import SurfaceType
from server.routes.pixel import Pixel
from server.routes.helper_debug.calculation_time import calculation_time

class DominateColor:
    ROUND_NUMBER = 2

    def __init__(self, img):
        self.__img = img

    def __round_color(self, color):
        return (round(color[0], self.ROUND_NUMBER), round(color[1], self.ROUND_NUMBER), round(color[2], self.ROUND_NUMBER))

    def get(self):
        count_color = {}
        max_row, max_col, z = self.__img.shape
        for i in range(1, 1000):
            row = random.randint(0, max_row - 1 )
            col = random.randint(0, max_col - 1)
            color = self.__round_color(self.__img[row][col])
            count_color[color] = count_color.get(color, 0) + 1
        max = 0
        max_color = None
        for color, count in count_color.items():
            if count > max:
                max = count
                max_color = color
        return max_color

class ImageCompression:
    COMPRESSION_SIZE = 10
    Z = 0.3**2
    def __init__(self, img, dominate_color):
        self.__img = img
        self.__dominate_color = dominate_color

    def isFreeSpace(self, row, column, max_row, max_col):
        r0, g0, b0 = self.__dominate_color
        for i in range(row, min(row + 10, max_row)):
            z = min(column + 10, max_col - 1)
            for j in range(column, min(column + 10, max_col)):
                r1, g1, b1, __ = self.__img[i][j]
                if abs(r1 - r0) + abs(g1 - g0) + abs(b1 - b0) >= self.Z:
                    return False
        return True

    @calculation_time
    def compress(self):
        max_row, max_col, z = self.__img.shape
        result = np.ndarray(
            shape=(max_row // self.COMPRESSION_SIZE, max_col // self.COMPRESSION_SIZE),
            dtype=Pixel
        )
        for index_row in range(0, max_row - self.COMPRESSION_SIZE, self.COMPRESSION_SIZE):
            for index_col in range(0, max_col - self.COMPRESSION_SIZE, self.COMPRESSION_SIZE):
                pixel = Pixel(np.zeros((3, )))
                res = self.isFreeSpace(index_row, index_col, max_row, max_col)
                if res == True:
                    pixel.surface = Surface(SurfaceType.FREE_SPACE)
                    pixel.surface.difficulty_overcome = 0.0
                else:
                    pixel.surface = Surface(SurfaceType.OBSTACLE)
                    pixel.surface.difficulty_overcome = 1.0
                result[index_row // self.COMPRESSION_SIZE, index_col // self.COMPRESSION_SIZE] = pixel
        return result

    @classmethod
    def convert_real_to_compress_coordinate(cls, coordinate):
        """
        Конвертировать реальные координаты в сжатые

        Args:
            coordinate (tuple): реальные координаты

        Returns:
            tuple: сжатые координаты
        """
        return coordinate[0] // cls.COMPRESSION_SIZE, coordinate[1] // cls.COMPRESSION_SIZE

    @classmethod
    def convert_compress_to_real_coordinate(cls, coordinate):
        """
        Конвертировать сжатые координаты в реальные

        Args:
            coordinate (tuple): реальные координаты

        Returns:
            tuple: сжатые координаты
        """
        return coordinate[0] * cls.COMPRESSION_SIZE, coordinate[1] * cls.COMPRESSION_SIZE
    '''
class ImageCompression:
    COMPRESSION_SIZE = 10
    SQR_COMPRESSION_SIZE = COMPRESSION_SIZE * COMPRESSION_SIZE

    def __init__(self, img):
        """
        Сжатие изображений

        Args:
            img (numpy.ndarray): изображение
        """
        self.__img = img


    @calculation_time
    def compress(self):
        """
        Сжать

        Returns:
            numpy.ndarray: сжатое изображение numpy.ndarray[numpy.ndarray[Pixel]]
        """
        pass

    @classmethod
    def convert_real_to_compress_coordinate(cls, coordinate):
        """
        Конвертировать реальные координаты в сжатые

        Args:
            coordinate (tuple): реальные координаты

        Returns:
            tuple: сжатые координаты
        """
        return coordinate[0] // cls.COMPRESSION_SIZE, coordinate[1] // cls.COMPRESSION_SIZE

    @classmethod
    def convert_compress_to_real_coordinate(cls, coordinate):
        """
        Конвертировать сжатые координаты в реальные

        Args:
            coordinate (tuple): реальные координаты

        Returns:
            tuple: сжатые координаты
        """
        return coordinate[0] * cls.COMPRESSION_SIZE, coordinate[1] * cls.COMPRESSION_SIZE
'''
