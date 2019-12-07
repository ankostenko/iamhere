import math
import itertools
import matplotlib.image as mpimg

from server.routes.way import Way
from server.routes.surface_type import SurfaceType
from server.routes.helper_debug.calculation_time import calculation_time
from server.routes.helper_debug.path_logs import PathLogs
from server.routes.image_compression import ImageCompression


class SearcherWay:
    """
    Класс который ищет путь
    """
    def __init__(self, pixels):
        """
        Конструктор

        Args:
            pixels (numpy.ndarray): поле пикселей numpy.ndarray<numpy.ndarray<pictures.pixel.Pixel>>
        """
        self.__pixels = pixels

    def __get_difficulty_overcome(self, row, col):
        """
        Получить сложность пути в данной точке
        Args:
            row (int): строчка
            col (int): колонка

        Returns:
            float: сложность пути
        """
        return self.__pixels[row][col].surface.difficulty_overcome

    @staticmethod
    def __get_find_way_difficulty(find_way):
        """
        Найти сложность уже найденного пути

        Args:
            find_way (pictures.way.Way, None): найденый путь

        Returns:
            float: сложность найденного пути
        """
        if find_way is None:
            return math.inf
        return find_way.full_difficulty

    def __clear_ways(self):
        """
        Очищает пути поиска
        """
        for pixel in itertools.chain.from_iterable(self.__pixels):
            if pixel is not None:
                pixel.way = None

    @calculation_time
    def find_way(self, start_point, end_point):
        """
        Поиск пути

        Args:
            start_point (tuple): стартовая позиция в форматье (row, col)
            end_point (tuple): конечная позиция в форматье (row, col)

        Returns:
            server.routes.way.Way: найденный путь
        """
        start_row, start_col = ImageCompression.convert_real_to_compress_coordinate(start_point)
        end_point = ImageCompression.convert_real_to_compress_coordinate(end_point)
        way_dict = {
            (start_row, start_col):
            Way(
                start_row,
                start_col,
                None,
                self.__get_difficulty_overcome(start_row, start_col)
            )
        }
        len_col, len_row = len(self.__pixels[0]), len(self.__pixels)
        find_way = None  # найденный путь
        while True:
            new_way_dict = {}
            for (row, col), way in way_dict.items():
                if way.short_way:
                    new_point_iterable = (
                        (new_row, new_col)
                        for new_row, new_col in
                        ((row, col - 1), (row, col + 1), (row - 1, col), (row + 1, col))
                        if 0 <= new_col < len_col and 0 <= new_row < len_row
                    )
                    for new_row, new_col in new_point_iterable:
                        new_pixel = self.__pixels[new_row][new_col]
                        surface = new_pixel.surface
                        if surface.surface_type == SurfaceType.FREE_SPACE:
                            new_way = Way(new_row, new_col, way, surface.difficulty_overcome)
                            if (
                                    new_way.is_short_way(new_pixel.way) and
                                    new_way.full_difficulty < self.__get_find_way_difficulty(find_way)
                            ):
                                new_way_dict[(new_row, new_col)] = new_way
                                new_pixel.way = new_way
                                # TODO тут вставка добавление дочерней
                                way.add_child_way(new_way)
                                if (new_row, new_col) == end_point:
                                    find_way = new_way
            if new_way_dict:
                way_dict = new_way_dict
            else:
                break
            # визуальный дебаг
            # print('---------- way ----------')
            # self.print_wave(new_way_dict)
        self.__clear_ways()
        return find_way

    @calculation_time
    def find_way_coordinate(self, way):
        """
        Нахождение пути результат в виде list[typle[row, col]]

        Args:
            way (Way): найденный путь

        Returns:
            list[typle[int, int]]: путь
        """
        result = []
        if way:
            previous_coordinate = ImageCompression.convert_compress_to_real_coordinate((way.row, way.col))
            result.append(previous_coordinate)

            direction = None
            way = way.parent_way
            while way is not None:
                next_coordinate = ImageCompression.convert_compress_to_real_coordinate((way.row, way.col))
                if direction is None:
                    direction = previous_coordinate[0] == next_coordinate[0]
                else:
                    next_direction = previous_coordinate[0] == next_coordinate[0]
                    if direction != next_direction:
                        result.append(previous_coordinate)
                        direction = next_direction

                way = way.parent_way
                if way is None:
                    result.append(next_coordinate)
                previous_coordinate = next_coordinate
        result.reverse()
        return result

    @calculation_time
    def print_way(self, find_way):
        """
        Распечатывает найденный путь

        Args:
            find_way (Way, None): найденный путь
        """
        way_set = set()
        while True:
            if find_way is not None:
                way_set.add((find_way.row, find_way.col))
                find_way = find_way.parent_way
            else:
                break

        for row, row_result in enumerate(self.__pixels):
            for col, type_result in enumerate(row_result):
                surface_type = type_result.surface.surface_type
                if(row, col) in way_set:
                    letter = '*'
                elif surface_type == SurfaceType.FREE_SPACE:
                    letter = ' '
                else:
                    letter = surface_type.name[0:1]
                print(letter, sep='', end='')
            print()

    @calculation_time
    def print_wave(self, wave):
        """
        Распечатывает найденный путь

        Args:
            wave (dict): волна распространения поиска
        """
        wave_set = set(key for key in wave.keys())

        for row, row_result in enumerate(self.__pixels):
            for col, type_result in enumerate(row_result):
                surface_type = type_result.surface.surface_type
                if(row, col) in wave_set:
                    letter = '*'
                elif surface_type == SurfaceType.FREE_SPACE:
                    letter = ' '
                else:
                    letter = surface_type.name[0:1]
                print(letter, sep='', end='')
            print()

    def __line(self, source_img, next_point, last_point):
        if last_point is not None:
            next_point = (
                ImageCompression.COMPRESSION_SIZE*next_point[0],
                ImageCompression.COMPRESSION_SIZE*next_point[1]
            )
            last_point = (
                ImageCompression.COMPRESSION_SIZE*last_point[0],
                ImageCompression.COMPRESSION_SIZE*last_point[1]
            )
            if next_point[0] == last_point[0]:
                rows = [next_point[0]] * ImageCompression.COMPRESSION_SIZE
                cols = range(
                    min(next_point[1], last_point[1]),
                    max(next_point[1], last_point[1])
                )
            else:
                rows = range(
                    min(next_point[0], last_point[0]),
                    max(next_point[0], last_point[0])
                )
                cols = [next_point[1]] * ImageCompression.COMPRESSION_SIZE

            for row, col in zip(rows, cols):
                source_img[row][col][0] = 1.0
                source_img[row][col][1] = 0.0
                source_img[row][col][2] = 0.5

    @calculation_time
    def save_file_way(self, find_way, source_img):
        """
        Отобразить найденный путь

        Args:
            find_way (Way, None): найденный путь
            source_img (numpy.ndarray): картинка
        """
        last_point = None
        while find_way is not None:
            point = find_way.row, find_way.col
            row, col = point
            source_img[row][col][0] = 1.0
            source_img[row][col][1] = 0.0
            source_img[row][col][2] = 0.5

            self.__line(source_img, point, last_point)
            last_point = point

            find_way = find_way.parent_way
        path = PathLogs.get_path_way()
        mpimg.imsave(path, source_img)
