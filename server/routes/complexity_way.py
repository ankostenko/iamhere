import math
import itertools
import matplotlib.image as mpimg
import re
import simplejson as json
import numpy as np
import os

from server.routes.surface_type import SurfaceType
from server.routes.surface import Surface
from server.routes.helper_debug.calculation_time import calculation_time
from server.routes.helper_debug.path_logs import PathLogs
from server.routes.image_compression import ImageCompression
from server.routes.pixel import Pixel


class ComplexityWay:
    """
    Нахождение сложности пути
    """
    DEFAULT_COMPLEXITY = 0.9

    def __init__(self, pixels):
        """
        Конструктор

        Args:
            pixels (list, numpy.ndarray): поле пикселей numpy.ndarray<numpy.ndarray<pictures.pixel.Pixel>>
        """
        self.__pixels = pixels

    def __get_obstacle_coordinates(self):
        """
        Получить координыты перпятствий

        Returns:
            generator: координаты припятствий
        """
        return itertools.chain.from_iterable(
            ((x, y) for x, pixel in enumerate(row) if pixel.surface.surface_type == SurfaceType.OBSTACLE)
            for y, row in enumerate(self.__pixels)
        )

    def __get_difficulty_overcome(self, step):
        """
        Вычислить сложность пути как расстояние от стенки
        Чем дальше от стенки тем проще идти
        1.0 - пройти нельзя
        0.0 - пройти не затрачивая сил

        Args:
            step (int): расстояние от стены

        Returns:
            float: сложность пути
        """
        return math.pow(self.DEFAULT_COMPLEXITY, step)

    @staticmethod
    def __get_json_file_patch(file_patch):
        """
        Имя файла для сохранения в json

        Args:
            file_patch (str): путь к файлу

        Returns:
            str: имя файла для сохранения в json
        """
        if file_patch:
            return os.path.splitext(file_patch)[0] + '_{}.json'.format(ImageCompression.COMPRESSION_SIZE)
        else:
            raise AttributeError('Не корректный путь(имя) файла: {0}'.format(file_patch))

    def __generator_complexity_patch(self):
        """
        Генератор сложности пути

        Yields:
            list: сложность пути с строчке
        """
        for row in self.__pixels:
            yield [pixel.surface.difficulty_overcome for pixel in row]

    @staticmethod
    def float_read_surface_type(float_str):
        """
        Преобразовать число сложности пути в класс пикселя

        Args:
            float_str (str): число в формате строки

        Returns:
            Pixel: разбирает пиксель из сложности
        """
        pixel = Pixel(np.zeros((3, )))
        if float_str == '1.0':
            pixel.surface = Surface(SurfaceType.OBSTACLE)
        else:
            pixel.surface = Surface(SurfaceType.FREE_SPACE)
            pixel.surface.difficulty_overcome = float(float_str)
        return pixel

    @calculation_time
    def find_complexity_way(self):
        """
        Расчитать сложность пути
        """
        step_coordinate = set(self.__get_obstacle_coordinates())
        new_step_coordinate = set()
        len_col, len_row = len(self.__pixels[0]), len(self.__pixels)
        for step in itertools.count():
            difficulty_overcome = self.__get_difficulty_overcome(step)
            for col, row in step_coordinate:
                self.__pixels[row][col].surface.difficulty_overcome = difficulty_overcome
                new_step_coordinate.update(
                    (new_col, new_row)
                    for new_col, new_row in
                    ((col - 1, row), (col + 1, row), (col, row - 1), (col, row + 1))
                    if (
                            0 <= new_col < len_col and 0 <= new_row < len_row and
                            self.__pixels[new_row][new_col].surface.difficulty_overcome == 0.
                    )
                )
            new_step_coordinate -= step_coordinate
            if not new_step_coordinate:
                break
            step_coordinate, new_step_coordinate = new_step_coordinate, set()

    @calculation_time
    def print_complexity_way(self):
        """
        Печать типа сложности подстилающей поверхности
        """
        for row_result in self.__pixels:
            for type_result in row_result:
                surface = type_result.surface
                surface_type = surface.surface_type
                print(
                    (
                        '##'
                        if surface_type == SurfaceType.OBSTACLE else
                        '{:>2}'.format(int(surface.difficulty_overcome * 100))
                    ),
                    sep='',
                    end=' '
                )
            print()

    @calculation_time
    def save_file_complexity_way(self, source_img):
        """
        Установить цвет
        свободного пространства - Белый
        цвет препятствий - Черный
        Сложность пути оттенки

        Args:
            source_img (numpy.ndarray): исходное изображение
        """
        for row_source, row_pixel in zip(source_img, self.__pixels):
            for source_pixel, pixel in zip(row_source, row_pixel):
                if pixel.surface.surface_type == SurfaceType.FREE_SPACE:
                    difficulty_overcome = pixel.surface.difficulty_overcome
                    source_pixel[0] = 1.0 - difficulty_overcome
                    source_pixel[1] = 1.0
                    source_pixel[2] = 1.0
        path = PathLogs.get_path_complex_way()
        mpimg.imsave(path, source_img)

    @classmethod
    def exists_complexity_way_to_json(cls, file_patch):
        """
        Проверяет существование предсохраненного файла со сложностемя пути

        Args:
            file_patch (str): путь к файлу с картинкой

        Returns:
            bool: существует ли такой файл
        """
        return os.path.isfile(cls.__get_json_file_patch(file_patch))

    def save_complexity_way_to_json(self, file_patch):
        """
        Соханить сложность пути в json
        1.0 --- не проходимо
        0.0 - 1.0 --- сложность пути

        Args:
            file_patch (str): имя файла открытого c картинкой.
        """
        with open(self.__get_json_file_patch(file_patch), 'w') as out_file:
            json.dump(self.__generator_complexity_patch(), out_file, iterable_as_array=True)

    @classmethod
    def load_complexity_way_from_json(cls, file_patch):
        """
        Загрузить сложность пути из файла
        1.0 --- не проходимо
        0.0 - 1.0 --- сложность пути

        Args:
            file_patch (str): имя файла открытого c картинкой.

        Returns:
            list: сложность пути list[list[Pixel]]
        """
        with open(cls.__get_json_file_patch(file_patch), "r") as read_file:
            pixels = json.load(read_file, parse_float=cls.float_read_surface_type)
            return pixels
