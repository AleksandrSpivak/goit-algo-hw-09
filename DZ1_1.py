import timeit
from typing import Callable


def find_coins_gready(coins, value):
    ccoins = coins.copy()
    change_dict = {}
    for coin in ccoins:
        if coin > 0:
            change_dict[coin] = value // int(coin)
            value = value % coin
    str = ", ".join(
        [
            f"монета {key}: {value} шт."
            for key, value in change_dict.items()
            if value > 0
        ]
    )

    return str


def find_min_coins(coins, sum_for_exchange):
    ccoins = coins.copy()
    ccoins.append(0)
    ccoins = ccoins[::-1]

    scenarios_matrix = [
        [0 for j in range(sum_for_exchange + 1)] for i in range(len(ccoins))
    ]

    scenarios_dict = {(0, j): {} for j in range(sum_for_exchange + 1)}

    i = 1
    for j in range(sum_for_exchange + 1):
        scenarios_matrix[i][j] = j
        scenario_current = {}
        scenario_current[i] = j
        scenarios_dict[(i, j)] = scenario_current

    for i in range(2, len(ccoins)):
        for j in range(sum_for_exchange + 1):
            if j < ccoins[i]:
                scenarios_matrix[i][j] = scenarios_matrix[i - 1][j]
                scenarios_dict[(i, j)] = scenarios_dict[(i - 1, j)]
            else:
                k = j // ccoins[i]
                scenarios_matrix[i][j] = k + scenarios_matrix[i][j % ccoins[i]]
                scenario_current = {}
                scenario_current[i] = k
                scenario_current |= scenarios_dict[(i, j % ccoins[i])]
                scenarios_dict[(i, j)] = scenario_current

    min_coins = scenarios_matrix[1][sum_for_exchange]
    solution = scenarios_dict[(1, sum_for_exchange)]
    for i in range(2, len(ccoins)):
        if scenarios_matrix[i][sum_for_exchange] < min_coins:
            min_coins = scenarios_matrix[i][sum_for_exchange]
            solution = scenarios_dict[(i, sum_for_exchange)]
    str = ", ".join(
        [
            f"монета {ccoins[key]}: {value} шт."
            for key, value in solution.items()
            if value > 0
        ]
    )
    return str


def benchmark(func: Callable, coins_, sum_for_exchange_):
    setup_code = f"from __main__ import {func.__name__}"
    stmt = f"{func.__name__}(coins, sum_for_exchange)"
    return timeit.timeit(
        stmt=stmt,
        setup=setup_code,
        globals={"coins": coins_, "sum_for_exchange": sum_for_exchange_},
        number=10,
    )


if __name__ == "__main__":
    coins = [50, 25, 10, 5, 2, 1]
    try:
        sum_for_exchange = int(input("Введіть необхідну для розміну суму: \n"))
        print("Результат жадібного алгоритму: ")
        print(find_coins_gready(coins, sum_for_exchange))
        print("Результат динамічного алгоритму: ")
        print(find_min_coins(coins, sum_for_exchange))
        if sum_for_exchange <= 0:
            raise ValueError
    except ValueError:
        print("не коректна сума")

    results = []
    for sum_for_exchange in [11, 111, 1111, 11111]:
        sum_res = []
        sum_res.append(sum_for_exchange)
        time = benchmark(find_coins_gready, coins, sum_for_exchange)
        sum_res.append(time)
        time = benchmark(find_min_coins, coins, sum_for_exchange)
        sum_res.append(time)
        results.append(sum_res)
    print("\nОбрахуємо час виконання алгоритмів за допомогою бібліотеки timeit:")
    print("Сума  | Жадібний алгоритм | Динамічний алгоритм")
    for result in results:
        print(f"{result[0]:<5} | {result[1]:<17f} | {result[2]:<17f}")
