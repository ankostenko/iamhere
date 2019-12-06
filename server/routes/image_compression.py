import numpy as np

from server.routes.pixel import Pixel
from server.routes.helper_debug.calculation_time import calculation_time


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

