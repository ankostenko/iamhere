class Way:
    """
    Путь
    """
    __slots__ = ('__row', '__col', '__parent_way', '__full_difficulty', '__short_way', '__child_ways')

    def __init__(self, row, col, parent_way, difficulty_overcome):
        """
        Конструктор

        Args:
            row (int): номер строки, координаты точки
            col (int): номер колонки, координаты точки
            parent_way (Way, None): родительская точка пути
            difficulty_overcome (float): длина данного участка пути
        """
        self.__row = row
        self.__col = col
        self.__parent_way = parent_way
        self.__full_difficulty = (
            difficulty_overcome
            if parent_way is None
            else self.__calc_full_difficulty(difficulty_overcome, parent_way)
        )
        self.__short_way = True
        self.__child_ways = []

    @staticmethod
    def __calc_full_difficulty(difficulty_overcome, parent_way):
        """
        Вычислить полную длительность(сложность) пути

        Args:
            difficulty_overcome (float): длина(сложность) данного участка пути
            parent_way (Way, None): родительская точка пути

        Returns:
            float: сложность пути
        """
        return parent_way.full_difficulty + difficulty_overcome

    @property
    def row(self):
        """
        int: номер строки, координаты точки
        """
        return self.__row

    @property
    def col(self):
        """
        int: номер колонки, координаты точки
        """
        return self.__col

    @property
    def parent_way(self):
        return self.__parent_way

    @property
    def full_difficulty(self):
        """
        float: полная длина(сложность) пути
        """
        return self.__full_difficulty

    @property
    def short_way(self):
        """
        bool: короткий путь
        """
        return self.__short_way

    def is_short_way(self, another_way):
        """
        Проверка являеться ли данный путь более короткий(простой)

        Args:
            another_way (Way, None): другой путь

        Returns:
            bool: более короткий(простой) путь
        """
        if another_way is None:
            return True
        short_way = self.full_difficulty < another_way.full_difficulty
        if short_way:
            another_way.set_not_short_way()
        return short_way

    def add_child_way(self, child_way):
        """
        Добавить путь который дочерний к текущему

        Args:
            child_way (Way): дочерний путь к данному
        """
        self.__child_ways.append(child_way)

    def set_not_short_way(self):
        """
        Проставляет что данный путь и все его дочерние больше не являеться самым коротким
        """
        self.__short_way = False
        for way in self.__child_ways:
            way.set_not_short_way()
