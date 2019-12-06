from enum import Enum, unique


@unique
class SurfaceType(Enum):
    """
    Тип поверхности
    """
    OBSTACLE = 1.0       # препятствие
    FREE_SPACE = 0.0     # свободное пространство

    @property
    def difficulty_overcome(self):
        """
        float: сложность преодаления(прохождения)
            1.0 - невозмлжно пройти
            0.0 - на преодаление не тратиться время
        """
        return self.value
