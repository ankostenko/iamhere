

class Surface:
    """
    Класс поверхность
    """
    __slots__ = ('__surface_type', '__difficulty_overcome')

    def __init__(self, surface_type):
        """
        КОнструктор

        Args:
            surface_type (pictures.surface_type.SurfaceType): тип поверхности
        """
        self.__surface_type = surface_type
        self.__difficulty_overcome = surface_type.difficulty_overcome

    @property
    def surface_type(self):
        return self.__surface_type

    @property
    def difficulty_overcome(self):
        """
        float: сложность преодаления(прохождения)
            1.0 - невозмлжно пройти
            0.0 - на преодаление не тратиться время
        """
        return self.__difficulty_overcome

    @difficulty_overcome.setter
    def difficulty_overcome(self, value):
        self.__difficulty_overcome = value
