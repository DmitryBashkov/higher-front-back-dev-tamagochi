"""Модуль со структурами игры"""


from game.models import Food, Medicine

# Еда
ALL_FOOD: tuple[Food, ...] = (
    Food(name='Бургер', satiety=20, price=40),
    Food(name='Салат', satiety=10, price=20),
    Food(name='Яблоко', satiety=10, price=15),
    Food(name='Пицца', satiety=35, price=60),
    Food(name='Картофель фри', satiety=25, price=30),
    Food(name='Свиные ребрышки', satiety=40, price=80),
)

# Лекарства
ALL_MEDICINE: tuple[Medicine, ...] = (
    Medicine(name='Ибупрофен', price=30, heal_hp=20, number_of_uses=2),
    Medicine(name='Цитрамон', price=15, heal_hp=10, number_of_uses=4),
    Medicine(name='Гастал', price=25, heal_hp=15, number_of_uses=3),
    Medicine(name='Смекта', price=20, heal_hp=10, number_of_uses=5),
    Medicine(name='Мезим', price=35, heal_hp=25, number_of_uses=2),
    Medicine(name='Пиво', price=10, heal_hp=5, number_of_uses=10),
)
