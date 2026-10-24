import os

from game.clicker import MyClicker
from game.exceptions import NotEnoughMoney
from game.game import MyGame
from game.structs import ALL_FOOD, ALL_MEDICINE
from game.tamagochi import MyTamagochi

STATUS_FORMAT = "Статус: голод {hunger}, здоровье {hp}, энергия {energy}, монет {coins}"
MENU_ITEMS = [
    "1. Пойти на работу",
    "2. Купить еду",
    "3. Купить лекарство",
    "4. Покормить",
    "5. Вылечить",
    "6. Играть",
    "7. Отдых",
    "0. Выход",
]
MENU_TEXT = "\n".join(MENU_ITEMS)


def main():
    tamagochi = MyTamagochi()
    clicker = MyClicker()
    game = MyGame(tamagochi, clicker, all_food=list(ALL_FOOD), all_medicine=list(ALL_MEDICINE))

    print("Добро пожаловать в Тамагочи-кликер!")
    output = ''

    while True:
        print(output)

        print(f"Сумка с едой: {game.food}")
        print(f"Сумка с лекарствами: {game.medicine}")

        status = game.get_status()
        print(f"\n{STATUS_FORMAT.format(**status)}\n")
        if status['is_sick']:
            print("=======Тамагочи болеет======")
            print("=======Отдых действует менее эффективно=======")
        print(MENU_TEXT)

        try:
            match input("Выберите действие: "):
                case "1":
                    income = game.work()
                    output = f'Вы заработали {income} монет'
                    game.tamagochi.update()
                case "2":
                    game.buy_food()
                    output = 'Еда куплена'
                case "3":
                    game.buy_medicine()
                    output = 'Лекарство куплено'
                case "4":
                    game.feed_tamagochi()
                case "5":
                    game.heal_tamagochi()
                case "6":
                    game.play_with_tamagochi()
                    output = 'Вы поиграли с питомцем'
                case "7":
                    game.rest_tamagochi()
                    output = 'Питомец отдохнул'
                case "0":
                    break
                case _:
                    output = "Неверная команда"
        except NotEnoughMoney as e:
            output = str(e)

        os.system('clear')


if __name__ == "__main__":
    main()
