"""Модуль с интерфейсом и реализацией кликера"""

import random
from abc import ABC, abstractmethod

from .consts import MAX_INCOME, MIN_INCOME


class AbstractClicker(ABC):
    """Интерфейс для кликера"""

    @abstractmethod
    def __init__(self) -> None:
        """Абстрактный метод инициализации"""
        raise NotImplementedError

    @abstractmethod
    def click(self) -> None:
        """Абстрактный метод клика для накапливания монет"""
        raise NotImplementedError

    @property
    @abstractmethod
    def income_per_click(self) -> int:
        """Абстрактное свойство для доступа к количеству монет за клик"""
        raise NotImplementedError


class MyClicker(AbstractClicker):
    """Класс кликера для заработка монет"""

    def __init__(self, min_income: int = MIN_INCOME, max_income: int = MAX_INCOME) -> None:
        """
        Инициализация кликера.

        :param min_income: минимальное количество монет за клик
        :param max_income: максимальное количество монет за клик
        """
        self._min_income = min_income
        self._max_income = max_income

    def click(self) -> int:
        """
        Выполняет клик и зарабатывает случайное количество монет.

        :return: количество заработанных монет
        """
        income = random.randint(self._min_income, self._max_income)
        return income

    @property
    def income_per_click(self) -> int:
        """
        Возвращает среднее количество монет за клик (min + max) // 2.

        :return: количество монет за клик
        """
        return (self._min_income + self._max_income) // 2
