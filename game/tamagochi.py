"""Модуль с интерфейсом и реализациями класса тамагочи"""

from abc import ABC, abstractmethod

from .consts import (
    DISEASE_CHANCE,
    ENERGY_DECREASE_MAX,
    ENERGY_DECREASE_MIN,
    FATIGUE_INCREASE_MAX,
    FATIGUE_INCREASE_MIN,
    FEED_ENERGY_DECREASE,
    HUNGER_INCREASE_MAX,
    HUNGER_INCREASE_MIN,
    MAX_ENERGY,
    MAX_FATIGUE,
    MAX_HP,
    MAX_HUNGER,
    PLAY_ENERGY_INCREASE,
    PLAY_FATIGUE_INCREASE,
    PLAY_HUNGER_INCREASE,
    REST_ENERGY_BONUS,
    REST_ENERGY_BONUS_SICK,
    REST_FATIGUE_DECREASE,
    REST_FATIGUE_DECREASE_SICK,
    REST_HP_BONUS,
    REST_HP_BONUS_SICK,
    SICK_FATIGUE_INCREASE,
    SICK_HP_DECREASE_MAX,
    SICK_HP_DECREASE_MIN,
    START_ENERGY,
    START_FATIGUE,
    START_HP,
    START_HUNGER,
)
from .models import Food, Medicine


class AbstractTamagochi(ABC):
    """Интерфейс логики тамагочи"""

    @abstractmethod
    def feed(self, food: Food) -> None:
        """
        Абстрактный метод для кормления тамагочи

        :param food: объект еды для кормления
        """
        raise NotImplementedError

    @abstractmethod
    def play(self) -> None:
        """Абстрактный метод для игры с тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def rest(self) -> None:
        """Абстрактный метод для отдыха тамагочи"""
        raise NotImplementedError

    @abstractmethod
    def heal(self, medicine: Medicine) -> None:
        """
        Абстрактный метод для лечения тамагочи

        :param medicine: лекарство для лечения
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def status(self) -> dict[str, int]:
        """
        Абстрактное свойство для доступа ко всем состояниям тамагочи

        :return: словарь со всеми состояниями тамагочи
        """
        raise NotImplementedError

    @abstractmethod
    def is_alive(self) -> bool:
        """
        Абстрактный метод для проверки жив ли тамагочи

        :return: True если жив, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def is_sick(self) -> bool:
        """
        Абстрактный метод для проверки, не заболел ли тамагочи

        :return: True если тамагочи болеет, иначе False
        """
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        """
        Абстрактный метод для обновления состояний тамагочи.
        Должен использоваться после каждого взаимодействия с тамагочи
        """
        raise NotImplementedError


class MyTamagochi(AbstractTamagochi):
    """Класс тамагочи с логикой игры"""

    def __init__(self) -> None:
        """
        Инициализация тамагочи с начальными состояниями.

        Начальные параметры:
        - hunger: START_HUNGER (голод на START_HUNGER%)
        - fatigue: START_FATIGUE (усталость START_FATIGUE%)
        - hp: START_HP (полное здоровье)
        - energy: START_ENERGY (энергия START_ENERGY%)
        - is_sick: False (не болен при создании)
        """
        self._hunger: int = START_HUNGER
        self._fatigue: int = START_FATIGUE
        self._hp: int = START_HP
        self._energy: int = START_ENERGY
        self._is_sick: bool = False
        self._max_values: dict[str, int] = {
            'hunger': MAX_HUNGER,
            'fatigue': MAX_FATIGUE,
            'hp': MAX_HP,
            'energy': MAX_ENERGY,
        }

    def feed(self, food: Food) -> None:
        """
        Кормит тамагочи указанной едой.

        :param food: объект еды для кормления
        """
        self._hunger = max(0, self._hunger - food.satiety)
        self._energy = max(0, self._energy - FEED_ENERGY_DECREASE)

    def play(self) -> None:
        """
        Играет с тамагочи.
        Повышает голод и усталость, снижает энергию.
        """
        self._hunger = min(self._max_values['hunger'], self._hunger + PLAY_HUNGER_INCREASE)
        self._fatigue = min(self._max_values['fatigue'], self._fatigue + PLAY_FATIGUE_INCREASE)
        self._energy = min(self._max_values['energy'], self._energy + PLAY_ENERGY_INCREASE)

    def rest(self) -> None:
        """
        Тамагочи отдыхает.
        Восстанавливает энергию, уменьшает усталость.
        При болезни эффект снижен в 2 раза.
        """
        if self._is_sick:
            self._energy = min(self._max_values['energy'], self._energy + REST_ENERGY_BONUS_SICK)
            self._fatigue = max(0, self._fatigue - REST_FATIGUE_DECREASE_SICK)
            self._hp = min(self._max_values['hp'], self._hp + REST_HP_BONUS_SICK)
        else:
            self._energy = min(self._max_values['energy'], self._energy + REST_ENERGY_BONUS)
            self._fatigue = max(0, self._fatigue - REST_FATIGUE_DECREASE)
            self._hp = min(self._max_values['hp'], self._hp + REST_HP_BONUS)

    def heal(self, medicine: Medicine) -> None:
        """
        Лечит тамагочи указанным лекарством.

        :param medicine: лекарство для лечения
        """
        if not medicine.is_empty():
            self._hp = min(self._max_values['hp'], self._hp + medicine.heal_hp)
            medicine.uses += 1

    @property
    def status(self) -> dict[str, int]:
        """
        Возвращает текущие состояния тамагочи.

        :return: словарь со всеми состояниями тамагочи
        """
        return {
            'hunger': self._hunger,
            'fatigue': self._fatigue,
            'hp': self._hp,
            'energy': self._energy,
        }

    def is_alive(self) -> bool:
        """
        Проверяет, жив ли тамагочи.

        :return: True если здоровье > 0, иначе False
        """
        return self._hp > 0

    def is_sick(self) -> bool:
        """
        Проверяет, болен ли тамагочи.

        :return: True если болеет, иначе False
        """
        return self._is_sick

    def update(self) -> None:
        """
        Обновляет состояние тамагочи.
        Повышает голод и усталость, снижает энергию.
        При болезни дополнительно снижает HP.
        Шанс заболевания — DISEASE_CHANCE.
        """
        import random

        if not self._is_sick and random.random() < DISEASE_CHANCE:
            self._is_sick = True

        self._hunger = min(self._max_values['hunger'], self._hunger + random.randint(HUNGER_INCREASE_MIN, HUNGER_INCREASE_MAX))
        self._fatigue = min(self._max_values['fatigue'], self._fatigue + random.randint(FATIGUE_INCREASE_MIN, FATIGUE_INCREASE_MAX))
        self._energy = max(0, self._energy - random.randint(ENERGY_DECREASE_MIN, ENERGY_DECREASE_MAX))

        if self._is_sick:
            self._hp -= random.randint(SICK_HP_DECREASE_MIN, SICK_HP_DECREASE_MAX)
            self._fatigue = min(self._max_values['fatigue'], self._fatigue + SICK_FATIGUE_INCREASE)
