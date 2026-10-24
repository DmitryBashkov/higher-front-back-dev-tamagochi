"""Модуль с константами игры"""

# Кликер
MIN_INCOME: int = 1
MAX_INCOME: int = 5

# Тамагочи - начальные значения
START_HUNGER: int = 50
START_FATIGUE: int = 20
START_HP: int = 100
START_ENERGY: int = 80

# Тамагочи - максимальные значения
MAX_HUNGER: int = 100
MAX_FATIGUE: int = 100
MAX_HP: int = 100
MAX_ENERGY: int = 100

# Тамагочи - прирост показателей при update()
HUNGER_INCREASE_MIN: int = 3
HUNGER_INCREASE_MAX: int = 5
FATIGUE_INCREASE_MIN: int = 2
FATIGUE_INCREASE_MAX: int = 4
ENERGY_DECREASE_MIN: int = 3
ENERGY_DECREASE_MAX: int = 6

# Тамагочи - болезнь
DISEASE_CHANCE: float = 0.1
SICK_HP_DECREASE_MIN: int = 1
SICK_HP_DECREASE_MAX: int = 2
SICK_FATIGUE_INCREASE: int = 5

# Тамагочи - эффекты действий
FEED_ENERGY_DECREASE: int = 5
PLAY_HUNGER_INCREASE: int = 10
PLAY_FATIGUE_INCREASE: int = 10
PLAY_ENERGY_INCREASE: int = 10
REST_ENERGY_BONUS: int = 20
REST_ENERGY_BONUS_SICK: int = 10
REST_FATIGUE_DECREASE: int = 20
REST_FATIGUE_DECREASE_SICK: int = 10
REST_HP_BONUS: int = 5
REST_HP_BONUS_SICK: int = 2

# Игра
START_COINS: int = 50
MAX_ITEMS: int = 10
