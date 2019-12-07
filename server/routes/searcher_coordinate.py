import math
import itertools
import matplotlib.image as mpimg

from server.routes.way import Way
from server.routes.surface_type import SurfaceType
from server.routes.helper_debug.calculation_time import calculation_time
from server.routes.helper_debug.path_logs import PathLogs
from server.routes.image_compression import ImageCompression
from server.routes.surface import Surface

class SearcherCoordinate:
    def __init__(self, point, pixels):
        self.__row, self.__col = ImageCompression.convert_real_to_compress_coordinate(point)
        self.__pixels = pixels
        self.__children = {(self.__row, self.__col)}
        self.__checked = {()}

    def get_coordinate(self):
        for i in self.__children:
            row, col = i
            if i not in self.__checked:
                if self.__pixels[row][col].surface.surface_type == SurfaceType.FREE_SPACE:
                    k = ImageCompression.convert_compress_to_real_coordinate((row, col))
                    return ImageCompression.convert_compress_to_real_coordinate((row, col))
                else:
                    new_children = self.__children
                    if (row + 1, col) not in self.__checked:
                        new_children.add((row + 1, col))
                    if (row - 1, col) not in self.__checked:
                        new_children.add((row - 1, col))
                    if (row, col + 1) not in self.__checked:
                        new_children.add((row, col + 1))
                    if (row, col - 1) not in self.__checked:
                        new_children.add((row, col - 1))
                    self.__checked.add((row, col))
                    self.__children = new_children
                    return self.get_coordinate()
