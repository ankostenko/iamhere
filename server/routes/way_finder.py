import matplotlib.image as mpimg
import cv2
from server.routes.identify_obstacles import IdentifyObstacles
from server.routes.complexity_way import ComplexityWay
from server.routes.searcher_way import SearcherWay
from server.routes.image_compression import ImageCompression
from server.routes.helper_debug.calculation_time import calculation_time
from server.routes.door_search import DoorSearch
from server.routes.image_compression import DominateColor
from server.routes.searcher_coordinate import SearcherCoordinate


class WayFinder:
    """
    Основной класс для поиска пути
    """
    def __init__(self, file_path):
        """
        Путь к файлу рисунка

        Args:
            file_path (str): путь к файлу рисунка
        """
        self.__file_path = file_path

    def get_complexity_way(self):
        """
        Получить предрасчеттаную сложность пути
        из файла если нет
        или рассчитать и записать в файл

        Returns:
            list, numpy.ndarray : предрасчитанная сложность пути
        """
        if ComplexityWay.exists_complexity_way_to_json(self.__file_path) is False:
            img = mpimg.imread(self.__file_path)

            image_compression = DominateColor(img)
            dominate_color = image_compression.get()

            image_compression = ImageCompression(img, dominate_color)
            compress_img = image_compression.compress()

            identify_obstacles = IdentifyObstacles(compress_img)
            identify_obstacles.find_obstacle_and_free_space()

            imgDoor = cv2.imread(self.__file_path)
            door = DoorSearch(imgDoor)
            door.Search(compress_img)

            complexity_way = ComplexityWay(compress_img)
            complexity_way.find_complexity_way()
            complexity_way.save_complexity_way_to_json(self.__file_path)
            return compress_img
        else:
            return ComplexityWay.load_complexity_way_from_json(self.__file_path)

    @calculation_time
    def find_way(self, start_row, start_col, end_row, end_col):
        """
        Найти путь из точки стартовой в конечную

        Args:
            start_row (int): строка стартовой точки
            start_col (int): колонка стартовой точки
            end_row (int): строка конечной точки
            end_col (int): колонка конечной точки

        Returns:
            list: список координат пути в формате list[tuple[row: int, col:int]]
        """
        # img = mpimg.imread(self.__file_path)
        #
        # image_compression = ImageCompression(img)
        # compress_img = image_compression.compress()
        #
        # identify_obstacles = IdentifyObstacles(compress_img)
        # identify_obstacles.find_obstacle_and_free_space()
        #
        # complexity_way = ComplexityWay(compress_img)
        # complexity_way.find_complexity_way()
        compress_img = self.get_complexity_way()

        searcher_way = SearcherWay(compress_img)
        fined_way = searcher_way.find_way(
            SearcherCoordinate((start_row, start_col), compress_img).get_coordinate(),
            SearcherCoordinate((end_row, end_col), compress_img).get_coordinate()
        )
        return searcher_way.find_way_coordinate(fined_way)
