"""Модуль с интерфейсом и реализацией класса игры."""

from abc import ABC, abstractmethod
from typing import Any, TypeVar

from .clicker import AbstractClicker
from .exceptions import NotEnoughMoney
from .models import Food, Medicine
from .tamagochi import AbstractTamagochi

Item = TypeVar("Item", Food, Medicine)


class AbstractGame(ABC):
    """Интерфейс для логики игры."""

    @abstractmethod
    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine]
    ):
        """
        Абстрактный метод инициализации класса игры.

        :param tamagochi: экземпляр тамагочи
        :param clicker: экземпляр кликера
        :param all_food: все доступные варианты еды
        :param all_medicine: все доступные варианты лекарств
        """
        raise NotImplementedError

    @abstractmethod
    def work(self) -> int:
        """
        Абстрактный метод для логики действия "работа".

        :return: количество заработанных монет
        """
        raise NotImplementedError

    @abstractmethod
    def buy_food(self) -> None:
        """Абстрактный метод для покупки еды."""
        raise NotImplementedError

    @abstractmethod
    def buy_medicine(self) -> None:
        """Абстрактный метод для покупки лекарства."""
        raise NotImplementedError

    @abstractmethod
    def feed_tamagochi(self) -> None:
        """Абстрактный метод для кормления тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def heal_tamagochi(self) -> None:
        """Абстрактный метод для лечения тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def rest_tamagochi(self):
        """Абстрактный метод для отдыха тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def play_with_tamagochi(self):
        """Абстрактный метод для игры с тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def get_status(self) -> dict[str, Any]:
        """
        Абстрактный метод для получения статуса (всех
        характеристик) тамагочи.

        :return: словарь со всеми характеристиками тамагочи
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def food(self) -> list[Food]:
        """
        Абстрактное свойство для доступа к сумке с едой.

        :return: список с имеющимися (купленными) объектами еды
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def medicine(self) -> list[Medicine]:
        """
        Абстрактное свойство для доступа к сумке с лекарствами.

        :return: список с имеющимися (купленными) объектами
        лекарств
        """
        raise NotImplementedError


class SimpleGame(AbstractGame):
    """Реализация игры: управление ресурсами и питомцем."""

    START_COINS: int = 50

    def __init__(
        self,
        tamagochi: AbstractTamagochi,
        clicker: AbstractClicker,
        all_food: list[Food],
        all_medicine: list[Medicine],
    ) -> None:
        """
        Инициализация игры.

        :param tamagochi: экземпляр тамагочи
        :param clicker: экземпляр кликера
        :param all_food: все доступные варианты еды
        :param all_medicine: все доступные варианты лекарств
        """
        self._tamagochi = tamagochi
        self._clicker = clicker
        self._all_food = list(all_food)
        self._all_medicine = list(all_medicine)
        self._food: list[Food] = []
        self._medicine: list[Medicine] = []
        self._coins = self.START_COINS

    @property
    def tamagochi(self) -> AbstractTamagochi:
        """
        Доступ к питомцу.

        :return: экземпляр тамагочи
        """
        return self._tamagochi

    def _choose_item(
        self,
        items: list[Item],
        title: str,
    ) -> Item | None:
        """
        Показывает пронумерованный список и читает выбор
        пользователя.

        :param items: доступные для выбора объекты
        :param title: название категории для сообщений
        :return: выбранный объект или None при пустом списке
        или некорректном вводе
        """
        if not items:
            print(f"Нет доступных позиций: {title}")
            return None
        for index, item in enumerate(items, start=1):
            print(f"{index}. {item}")
        choice = input("Выберите позицию: ").strip()
        if not choice.isdigit():
            print("Неверный ввод")
            return None
        position = int(choice)
        if not 1 <= position <= len(items):
            print("Неверный ввод")
            return None
        return items[position - 1]

    def _spend_coins(self, price: int) -> None:
        """
        Списывает монеты за покупку.

        :param price: стоимость покупки
        :raises NotEnoughMoney: если монет недостаточно
        """
        if self._coins < price:
            raise NotEnoughMoney(
                f"Не хватает монет: {price - self._coins}",
            )
        self._coins -= price

    def work(self) -> int:
        """
        Ход действия «пойти на работу».

        Зарабатывает монеты кликером и переводит игровой
        тик.

        :return: количество заработанных монет
        """
        self._clicker.click()
        income = self._clicker.income_per_click
        self._coins += income
        self._tamagochi.update()
        return income

    def buy_food(self) -> None:
        """
        Логика действия «покупка еды».

        :raises NotEnoughMoney: если монет не хватает
        """
        food = self._choose_item(self._all_food, "еда")
        if food is None:
            return
        self._spend_coins(food.price)
        self._food.append(food)
        print(f"Куплено: {food.name}")

    def buy_medicine(self) -> None:
        """
        Логика действия «купить лекарство».

        :raises NotEnoughMoney: если монет не хватает
        """
        medicine = self._choose_item(
            self._all_medicine,
            "лекарство",
        )
        if medicine is None:
            return
        self._spend_coins(medicine.price)
        self._medicine.append(medicine)
        print(f"Куплено: {medicine.name}")

    def feed_tamagochi(self) -> None:
        """Логика действия «покормить питомца»."""
        food = self._choose_item(self._food, "еда")
        if food is None:
            return
        self._food.remove(food)
        self._tamagochi.feed(food)
        self._tamagochi.update()

    def heal_tamagochi(self) -> None:
        """Логика действия «вылечить питомца»."""
        medicine = self._choose_item(
            self._medicine,
            "лекарство",
        )
        if medicine is None:
            return
        self._tamagochi.heal(medicine)
        if medicine.is_empty():
            self._medicine.remove(medicine)
        self._tamagochi.update()

    def rest_tamagochi(self) -> None:
        """Логика действия «отдых»."""
        self._tamagochi.rest()
        self._tamagochi.update()

    def play_with_tamagochi(self) -> None:
        """Логика действия «поиграть с питомцем»."""
        self._tamagochi.play()
        self._tamagochi.update()

    def get_status(self) -> dict[str, Any]:
        """
        Статус игры: показатели питомца и монеты.

        :return: словарь со всеми характеристиками игры
        """
        return {
            **self._tamagochi.status,
            "coins": self._coins,
        }

    @property
    def food(self) -> list[Food]:
        """
        Сумка с едой.

        :return: список купленной еды
        """
        return self._food

    @property
    def medicine(self) -> list[Medicine]:
        """
        Сумка с лекарствами.

        :return: список купленных лекарств
        """
        return self._medicine
