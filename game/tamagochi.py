"""Модуль с интерфейсом и реализациями класса тамагочи."""

import random
from abc import ABC, abstractmethod

from .exceptions import TamagochiIsGone
from .models import Food, Medicine


class AbstractTamagochi(ABC):
    """Интерфейс логики тамагочи."""

    @abstractmethod
    def feed(self, food: Food) -> None:
        """
        Абстрактный метод для кормления тамагочи.

        :param food: объект еды для кормления
        """
        raise NotImplementedError

    @abstractmethod
    def play(self) -> None:
        """Абстрактный метод для игры с тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def rest(self) -> None:
        """Абстрактный метод для отдыха тамагочи."""
        raise NotImplementedError

    @abstractmethod
    def heal(self, medicine: Medicine) -> None:
        """
        Абстрактный метод для лечения тамагочи.

        :param medicine: лекарство для лечения
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def status(self) -> dict[str, int]:
        """
        Абстрактное свойство для доступа ко всем состояниям тамагочи.

        :return: словарь со всеми состояниями тамагочи
        """
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """
        Абстрактный метод для проверки жив ли тамагочи.

        :return: True если жив, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def is_sick(self) -> bool:
        """
        Абстрактный метод для проверки, не заболел ли тамагочи.

        :return: True если тамагочи болеет, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        """
        Абстрактный метод для обновления состояний тамагочи.

        Должен использоваться после каждого взаимодействия
        с тамагочи.
        """
        raise NotImplementedError


class SimpleTamagochi(AbstractTamagochi):
    """Реализация тамагочи с показателями голода, HP и энергии."""

    MAX_HUNGER: int = 100
    MAX_HP: int = 100
    MAX_ENERGY: int = 100
    START_HUNGER: int = 0

    HUNGER_PER_TICK: int = 5
    ENERGY_PER_TICK: int = 3
    SICK_CHANCE: float = 0.1
    SICK_DAMAGE: int = 5
    STARVE_DAMAGE: int = 10

    PLAY_ENERGY_COST: int = 10
    PLAY_HUNGER_COST: int = 5
    REST_ENERGY: int = 30
    SICK_REST_PENALTY: int = 2

    def __init__(self) -> None:
        """Инициализация тамагочи стартовыми показателями."""
        self._hunger: int = self.START_HUNGER
        self._hp: int = self.MAX_HP
        self._energy: int = self.MAX_ENERGY
        self._is_sick: bool = False

    def feed(self, food: Food) -> None:
        """
        Кормление тамагочи: уменьшает голод.

        :param food: объект еды для кормления
        """
        self._hunger = max(0, self._hunger - food.satiety)

    def play(self) -> None:
        """Игра с тамагочи: тратит энергию и усиливает голод."""
        self._energy = max(
            0,
            self._energy - self.PLAY_ENERGY_COST,
        )
        self._hunger = min(
            self.MAX_HUNGER,
            self._hunger + self.PLAY_HUNGER_COST,
        )

    def rest(self) -> None:
        """Отдых тамагочи: восстанавливает энергию.

        Во время болезни отдых действует менее эффективно.
        """
        gain = self.REST_ENERGY
        if self._is_sick:
            gain //= self.SICK_REST_PENALTY
        self._energy = min(self.MAX_ENERGY, self._energy + gain)

    def heal(self, medicine: Medicine) -> None:
        """
        Лечение тамагочи: восстанавливает HP и снимает болезнь.

        Пустое лекарство не применяется.

        :param medicine: лекарство для лечения
        """
        if medicine.is_empty():
            return
        medicine.uses += 1
        self._hp = min(self.MAX_HP, self._hp + medicine.heal_hp)
        self._is_sick = False

    @property
    def status(self) -> dict[str, int]:
        """
        Текущие показатели тамагочи.

        :return: словарь с показателями голода, HP и энергии
        """
        return {
            "hunger": self._hunger,
            "hp": self._hp,
            "energy": self._energy,
        }

    def is_alive(self) -> bool:
        """
        Проверка, жив ли тамагочи.

        :return: True если HP больше нуля, иначе False
        """
        return self._hp > 0

    def is_sick(self) -> bool:
        """
        Проверка, болеет ли тамагочи.

        :return: True если тамагочи болеет, иначе False
        """
        return self._is_sick

    def update(self) -> None:
        """
        Обновление состояний тамагочи (один тик игры).

        Со временем голод растёт, энергия падает, тамагочи
        может заболеть. Голодный или больной тамагочи теряет HP.

        :raises TamagochiIsGone: если HP упал до нуля
        """
        if not self.is_alive():
            raise TamagochiIsGone("Питомец погиб")
        self._hunger = min(
            self.MAX_HUNGER,
            self._hunger + self.HUNGER_PER_TICK,
        )
        self._energy = max(
            0,
            self._energy - self.ENERGY_PER_TICK,
        )
        if not self._is_sick:
            self._is_sick = (
                random.random() < self.SICK_CHANCE
            )
        if self._is_sick:
            self._hp -= self.SICK_DAMAGE
        if self._hunger >= self.MAX_HUNGER:
            self._hp -= self.STARVE_DAMAGE
        self._hp = max(0, self._hp)
        if self._hp <= 0:
            raise TamagochiIsGone("Питомец погиб")
