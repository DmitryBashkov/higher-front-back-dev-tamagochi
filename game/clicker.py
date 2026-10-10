"""Модуль с интерфейсом и реализацией кликера."""

import random
from abc import ABC, abstractmethod


class AbstractClicker(ABC):
    """Интерфейс для кликера."""

    @abstractmethod
    def __init__(self) -> None:
        """Абстрактный метод инициализации."""
        raise NotImplementedError

    @abstractmethod
    def click(self) -> None:
        """Абстрактный метод клика для накапливания монет."""
        raise NotImplementedError

    @property
    @abstractmethod
    def income_per_click(self) -> int:
        """Абстрактное свойство для доступа к количеству монет за клик."""
        raise NotImplementedError


class SimpleRandomClicker(AbstractClicker):
    """Кликер со случайным доходом за клик в заданном диапазоне."""

    def __init__(
        self,
        min_income: int = 1,
        max_income: int = 10,
    ) -> None:
        """
        Инициализация кликера.

        :param min_income: минимальный доход за один клик
        :param max_income: максимальный доход за один клик
        :raises ValueError: если min_income больше max_income
        """
        if min_income > max_income:
            raise ValueError(
                "min_income не может быть больше max_income",
            )
        self._min_income = min_income
        self._max_income = max_income
        self._last_income = min_income

    @property
    def income_per_click(self) -> int:
        """
        Доход за последний выполненный клик.

        :return: количество монет, заработанных за клик
        """
        return self._last_income

    def click(self) -> None:
        """Выполняет клик и запоминает случайный доход."""
        self._last_income = random.randint(
            self._min_income,
            self._max_income,
        )
