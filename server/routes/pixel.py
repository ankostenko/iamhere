import math
import numpy as np


class Pixel:
    """
    Класс пикселя
    """
    __slots__ = ('__pixel', '__surface', '__way')

    def __init__(self, pixel):
        """
        Конструктор

        Args:
            pixel (numpy.ndarray): цвет пицеля
        """
        self.__pixel = pixel
        self.__surface = None
        self.__way = None

    @property
    def red(self):
        return self.__pixel[0]

    @red.setter
    def red(self, value):
        self.__pixel[0] = value

    @property
    def green(self):
        return self.__pixel[1]

    @green.setter
    def green(self, value):
        self.__pixel[1] = value

    @property
    def blue(self):
        return self.__pixel[2]

    @blue.setter
    def blue(self, value):
        self.__pixel[2] = value

    def difference(self, pixel):
        """
        Сравнение похожести 2-х пикселей
        среднее по квадратам разности по цветам

        Args:
            pixel (Pixel): пиксель

        Returns:
            float: степень похожести.
                0 - очень похожи 1 - совсем разные
        """
        return math.sqrt(
            math.pow(self.red - pixel.red, 2) +
            math.pow(self.green - pixel.green, 2) +
            math.pow(self.blue - pixel.blue, 2)
        )

    def deep(self):
        """
        Глубина цвета

        Returns:
            float: глубина цвета
        """
        return self.difference(Pixel(np.zeros((3, ))))

    def round(self, number):
        """
        Округление цвета

        Args:
            number (int): глубина округления
        """
        self.__pixel[0] = round(self.__pixel[0], number)
        self.__pixel[1] = round(self.__pixel[1], number)
        self.__pixel[2] = round(self.__pixel[2], number)

    @property
    def surface(self):
        """
        server.routes.surface.Surface : тип поверхности
        """
        return self.__surface

    @surface.setter
    def surface(self, value):
        self.__surface = value

    @property
    def way(self):
        """
        server.routes.way.Way: Путь который ищеться от точки до точки
        """
        return self.__way

    @way.setter
    def way(self, value):
        self.__way = value

    def __eq__(self, obj):
        """
        Сравнение 2-х элементов

        Args:
            obj (object): сравниваемый элемент

        Returns:

        """
        if not isinstance(obj, Pixel):
            return False
        if self.red == obj.red and self.blue == obj.blue and self.green == obj.green:
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.red, self.green, self.blue))

    def __repr__(self):
        return 'Pixel(R: {:.3} G: {:.3} B: {:.3} Surface:{:.3})'.format(
            self.red,
            self.green,
            self.blue,
            self.surface.difficulty_overcome if self.surface else 0.)
