from datetime import datetime
import os


class PathLogs:
    """
    Путь к логам выполнения скрипта
    """
    PATH_FORMAT = "%Y %m %d - %H %M %S"
    PATH = None
    OBSTACLES = 'obstacles.png'
    COMPLEX_WAY = 'complex_way.png'
    WAY = 'way.png'

    @classmethod
    def get_path(cls):
        """
        Путь к логам скрипта

        Returns:
            str: путь к логам скрипта
        """
        if cls.PATH is None:
            directory = os.getcwd() + os.sep + 'logs'
            if os.path.isdir(directory) is False:
                os.mkdir(directory)
            cls.PATH = directory + os.sep + datetime.strftime(datetime.now(), cls.PATH_FORMAT)
            os.mkdir(cls.PATH)
        return cls.PATH

    @classmethod
    def get_path_obstacles_file(cls):
        """
        Путь к разобранному файлу препятсвия свободное пространоство

        Returns:
            str: путь к файлу препятсвий свободного пространостра
        """
        return cls.get_path() + os.sep + cls.OBSTACLES

    @classmethod
    def get_path_complex_way(cls):
        """
        Путь к разобранному файлу препятсвия
        сложность пути

        Returns:
            str: путь к файлу препятсвий свободного пространостра
        """
        return cls.get_path() + os.sep + cls.COMPLEX_WAY

    @classmethod
    def get_path_way(cls):
        """
        Путь к разобранному файлу пути

        Returns:
            str: путь к файлу препятсвий свободного пространостра
        """
        return cls.get_path() + os.sep + cls.WAY
