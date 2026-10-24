"""Модуль с интерфейсом и реализацией класса игры"""

from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Any

from .clicker import AbstractClicker
from .consts import MAX_ITEMS, START_COINS
from .exceptions import NotEnoughMoney
from .models import Food, Medicine
from .structs import ALL_FOOD, ALL_MEDICINE
from .tamagochi import AbstractTamagochi


class AbstractGame(ABC):
    """Интерфейс для логики игры"""

    @abstractmethod
    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine]
    ):
        """
        Абстрактный метод инициализации класса игры

        :param tamagochi: экземпляр тамагочи
        :param clicker: экземпляр кликера
        :param all_food: все доступные варианты еды
        :param all_medicine: все доступные варианты лекарств
        """
        raise NotImplementedError

    @abstractmethod
    def work(self) -> int:
        """
        Абстрактный метод для логики действия "работа

        :return: количество заработанных монет
        """
        raise NotImplementedError

    @abstractmethod
    def buy_food(self) -> None:
        """Абстрактный метод для покупки еды"""
        raise NotImplementedError

    @abstractmethod
    def buy_medicine(self) -> None:
        """Абстрактный метод для покупки лекарства"""
        raise NotImplementedError

    @abstractmethod
    def feed_tamagochi(self) -> None:
        """Абстрактный метод для кормления тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def heal_tamagochi(self) -> None:
        """Абстрактный метод для лечения тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def rest_tamagochi(self):
        """Абстрактный метод для отдыха тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def play_with_tamagochi(self):
        """Абстрактный метод для игры с тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        """
        Абстрактный метод для получения статуса (всех характеристик) тамагочи

        :return: словарь со всеми характеристиками тамагочи
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def food(self) -> list[Food]:
        """
        Абстрактное свойство для доступа к сумке с едой

        :return: список с имеющимися (купленными) объектами еды
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def medicine(self) -> list[Medicine]:
        """
        Абстрактное свойство для доступа к сумке с лекарствами

        :return: список с имеющимися (купленными) объектами лекарств
        """
        raise NotImplementedError


class MyGame(AbstractGame):
    """Класс игры, управляющий всеми компонентами"""

    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food] | None = None,
        all_medicine: list[Medicine] | None = None,
        start_coins: int = START_COINS,
        max_items: int = MAX_ITEMS
    ):
        """
        Инициализация игры.

        :param tamagochi: экземпляр тамагочи
        :param clicker: экземпляр кликера
        :param all_food: все доступные варианты еды (если None, используются из structs)
        :param all_medicine: все доступные варианты лекарств (если None, используются из structs)
        :param start_coins: начальное количество монет
        :param max_items: максимальное количество предметов в сумке
        """
        self._tamagochi = tamagochi
        self._clicker = clicker
        self._all_food = list(deepcopy(ALL_FOOD)) if all_food is None else list(deepcopy(all_food))
        self._all_medicine = list(deepcopy(ALL_MEDICINE)) if all_medicine is None else list(deepcopy(all_medicine))
        self._coins = start_coins
        self._max_items = max_items
        self._food_bag: list[Food] = []
        self._medicine_bag: list[Medicine] = []

    def work(self) -> int:
        """
        Работает и зарабатывает монеты через кликер.
        Вызывает update() у тамагочи после заработка.

        :return: количество заработанных монет
        """
        self._clicker.click()
        income = self._clicker.income_per_click
        self._coins += income
        self._tamagochi.update()
        return income

    def buy_food(self) -> None:
        """
        Покупает еду. Выбирает самую дешёвую доступную еду.
        Проверяет наличие денег и места в сумке.

        :raises NotEnoughMoney: если недостаточно монет для покупки
        """
        if not self._all_food:
            return

        if len(self._food_bag) >= self._max_items:
            return

        food_to_buy = min(self._all_food, key=lambda f: f.price)
        if self._coins >= food_to_buy.price:
            self._coins -= food_to_buy.price
            self._food_bag.append(food_to_buy)
        else:
            raise NotEnoughMoney("Недостаточно монет для покупки еды")

    def buy_medicine(self) -> None:
        """
        Покупает лекарство. Выбирает первое доступное лекарство.
        Проверяет наличие денег и места в сумке.

        :raises NotEnoughMoney: если недостаточно монет для покупки
        """
        if not self._all_medicine:
            return

        if len(self._medicine_bag) >= self._max_items:
            return

        medicine_to_buy = self._all_medicine[0]
        if self._coins >= medicine_to_buy.price:
            self._coins -= medicine_to_buy.price
            self._medicine_bag.append(medicine_to_buy)
        else:
            raise NotEnoughMoney("Недостаточно монет для покупки лекарства")

    def feed_tamagochi(self) -> None:
        """
        Кормит тамагочи. Выбирает самую калорийную доступную еду.
        """
        if not self._food_bag:
            return

        food_to_feed = max(self._food_bag, key=lambda f: f.satiety)
        self._food_bag.remove(food_to_feed)
        self._tamagochi.feed(food_to_feed)
        self._tamagochi.update()

    def heal_tamagochi(self) -> None:
        """
        Лечит тамагочи. Использует первое доступное лекарство.
        """
        if not self._medicine_bag:
            return

        medicine_to_heal = self._medicine_bag[0]
        if not medicine_to_heal.is_empty():
            self._tamagochi.heal(medicine_to_heal)
            self._tamagochi.update()

    def rest_tamagochi(self) -> None:
        """Позволяет тамагочи отдохнуть."""
        self._tamagochi.rest()
        self._tamagochi.update()

    def play_with_tamagochi(self) -> None:
        """Играет с тамагочи."""
        self._tamagochi.play()
        self._tamagochi.update()

    def get_status(self) -> dict[str, Any]:
        """
        Возвращает статус игры и тамагочи.

        :return: словарь со всеми характеристиками
        """
        tamagochi_status = self._tamagochi.status
        return {
            'hunger': tamagochi_status['hunger'],
            'fatigue': tamagochi_status['fatigue'],
            'hp': tamagochi_status['hp'],
            'energy': tamagochi_status['energy'],
            'coins': self._coins,
            'is_sick': self._tamagochi.is_sick(),
        }

    @property
    def food(self) -> list[Food]:
        """
        Возвращает список еды в сумке.

        :return: список с имеющимися объектами еды
        """
        return self._food_bag

    @property
    def medicine(self) -> list[Medicine]:
        """
        Возвращает список лекарств в сумке.

        :return: список с имеющимися объектами лекарств
        """
        return self._medicine_bag

    @property
    def tamagochi(self) -> AbstractTamagochi:
        """
        Возвращает экземпляр тамагочи.

        :return: экземпляр тамагочи
        """
        return self._tamagochi
