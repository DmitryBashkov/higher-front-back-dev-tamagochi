import os

from game.clicker import SimpleRandomClicker
from game.exceptions import NotEnoughMoney, TamagochiIsGone
from game.game import SimpleGame
from game.models import Food, Medicine
from game.tamagochi import SimpleTamagochi


def main() -> None:
    """Точка входа: событийный цикл игры."""
    all_food = [
        Food(name="Бургер", satiety=20, price=40),
        Food(name="Салат", satiety=10, price=20),
        Food(name="Яблоко", satiety=10, price=15),
    ]

    all_medicine = [
        Medicine(
            name="Ибупрофен",
            price=30,
            heal_hp=20,
            number_of_uses=2,
        )
    ]

    tamagochi = SimpleTamagochi()
    clicker = SimpleRandomClicker(10, 20)
    game = SimpleGame(
        tamagochi,
        clicker,
        all_food=all_food,
        all_medicine=all_medicine,
    )

    print("Добро пожаловать в Тамагочи-кликер!")
    output = ""

    try:
        while True:
            print(output)

            print(f"Сумка с едой: {game.food}")
            print(f"Сумка с лекарствами: {game.medicine}")

            status = game.get_status()
            print(
                f"\nСтатус: голод {status['hunger']}, "
                f"здоровье {status['hp']}, "
                f"энергия {status['energy']}, "
                f"монет {status['coins']}\n"
            )
            if game.tamagochi.is_sick():
                print("=======Тамагочи болеет======")
                print("=======Отдых действует менее"
                      " эффективно=======")
            print("1. Пойти на работу")
            print("2. Купить еду")
            print("3. Купить лекарство")
            print("4. Покормить")
            print("5. Вылечить")
            print("6. Играть")
            print("7. Отдых")
            print("0. Выход")

            match input("Выберите действие: "):
                case "1":
                    output = (
                        f"Вы заработали {game.work()} монет"
                    )
                case "2":
                    try:
                        game.buy_food()
                    except NotEnoughMoney as error:
                        output = str(error)
                case "3":
                    try:
                        game.buy_medicine()
                    except NotEnoughMoney as error:
                        output = str(error)
                case "4":
                    game.feed_tamagochi()
                case "5":
                    game.heal_tamagochi()
                case "6":
                    game.play_with_tamagochi()
                    output = "Вы поиграли с питомцем"
                case "7":
                    game.rest_tamagochi()
                    output = "Питомец отдохнул"
                case "0":
                    break
                case _:
                    output = "Неверная команда"

            os.system("clear")
    except TamagochiIsGone:
        print("Питомец погиб. Игра окончена.")


if __name__ == "__main__":
    main()
