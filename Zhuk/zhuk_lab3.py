from tabulate import tabulate
import random

def Alex_strategy(**kwargs):
    return 1

def Bob_strategy(**kwargs):
    return 0

def Clara_strategy(**kwargs):
    if kwargs["part_count"] == 1:
        return 0

    return kwargs["last_opponent"]

def Denis_strategy(**kwargs):
    if kwargs["part_count"] == 1:
        return 0

    if kwargs["last_opponent"] == 1:
        return 0
    return 1

def Emma_strategy(**kwargs):
    if kwargs["part_count"] % 20 == 0:
        return 1
    return 0

def Frida_strategy(**kwargs):
    if kwargs["part_count"] == 1:
        Frida_strategy.decis = 0

    if kwargs["last_opponent"] == 1:
        Frida_strategy.decis = 1

    return Frida_strategy.decis

def George_strategy(**kwargs):
    if kwargs["part_count"] == 1:
        George_strategy.betrayal_count = 0
        return 0

    if kwargs["last_opponent"] == 1:
        George_strategy.betrayal_count += 1

    if George_strategy.betrayal_count >= GAME_COUNT // 4:
        return 1

    return kwargs["last_opponent"]

def Hank_strategy(**kwargs):
    return 0 if random.random() <= 0.5 else 1

def Ivan_strategy(**kwargs):
    return 0 if random.random() <= 0.9 else 1

def Jack_strategy(**kwargs):
    if kwargs["part_count"] == 1:
        return 0

    if kwargs["last_opponent"] == 1:
        return 0 if random.random() <= 0.25 else 1
    return 0

def Kevin_strategy(**kwargs):
    if kwargs["part_count"] == 1:
        return 0

    if kwargs["last_opponent"] == 1:
        return 0 if random.random() <= 0.25 else 1
    else:
        return 1 if random.random() <= 0.25 else 0

def Lucas_strategy(**kwargs):
    if kwargs["part_count"] == 1:
        Lucas_strategy.interval_between_one = random.randint(1,50)

    return 1 if kwargs["part_count"] % Lucas_strategy.interval_between_one == 0 else 0

def Max_strategy(**kwargs):
    if kwargs["part_count"] == 1:
        Max_strategy.interval_between_one_and_zero = random.randint(1, 20)
        Max_strategy.parti_counter = 1
        Max_strategy.is_one = False

    result = 0 if not Max_strategy.is_one else 1
    if Max_strategy.parti_counter >= Max_strategy.interval_between_one_and_zero:
        Max_strategy.is_one = True if not Max_strategy.is_one else False
        Max_strategy.parti_counter = 0
        Max_strategy.interval_between_one_and_zero = random.randint(1, 20)

    Max_strategy.parti_counter += 1
    return result

def Natan_strategy(**kwargs):
    if kwargs["part_count"] == 1:
        Natan_strategy.level_of_trust = 0.5

    if kwargs["last_opponent"] == 1:
        if Natan_strategy.level_of_trust != 0.1:
            Natan_strategy.level_of_trust -= 0.1
    else:
        if Natan_strategy.level_of_trust != 0.9:
            Natan_strategy.level_of_trust += 0.1

    return 0 if random.random() <= Natan_strategy.level_of_trust else 1

def count_dispersi(selection, middle_value):
    sqr_sum = 0
    for sel in selection:
        sqr_sum += (sel - middle_value) ** 2

    return sqr_sum / (len(selection) - 1)

def count_median(selection):
    selection.sort()
    return (selection[len(selection) // 2] + selection[len(selection) // 2 - 1]) // 2

def count_moda(selection):
    frequency = {(-1, 100) : [],
                 (100, 200) : [],
                 (200, 300) : [],
                 (300, 400) : [],
                 (400, 500) : [],
                 (500, 600) : [],
                 (600, 700) : [],
                 (700, 800) : [],
                 (800, 900) : [],
                 (900, 1000) : []
                 }

    for interval in frequency:
        for sel in selection:
            if interval[0] < sel <= interval[1]:
                frequency[interval].append(sel)

    key_with_max_value = max(frequency, key = lambda x: len(frequency[x]))
    return sum(frequency[key_with_max_value]) / len(frequency[key_with_max_value])


W = ((3, 0),
     (5, 1))
SIMULATES_COUNT = 1000
GAME_COUNT = 200
participants = {
    "Alex": Alex_strategy,
    "Bob": Bob_strategy,
    "Clara": Clara_strategy,
    "Denis": Denis_strategy,
    "Emma": Emma_strategy,
    "Frida": Frida_strategy,
    "George": George_strategy,
    "Hank": Hank_strategy,
    "Ivan": Ivan_strategy,
    "Jack": Jack_strategy,
    "Kevin": Kevin_strategy,
    "Lucas": Lucas_strategy,
    "Max": Max_strategy,
    "Natan": Natan_strategy
}

def main():

    part_keys = list(participants)
    middle_values_result = []
    dispersi_values_result = []
    median_values_result = []
    moda_values_result = []

    for first_parti in part_keys:
        middle_values, dispersi_values, median_values, mode_values = [], [], [], []
        for second_parti in part_keys:
            selection = []
            for simulation in range(SIMULATES_COUNT):
                last_opponent_for_first, last_opponent_for_second = 0, 0
                first_opponent_score = 0
                for game_count in range(1, GAME_COUNT + 1):

                    f_op_decision = participants[first_parti](last_opponent = last_opponent_for_first, part_count = game_count)

                    sec_op_desicion = participants[second_parti](last_opponent = last_opponent_for_second, part_count = game_count)

                    last_opponent_for_first = sec_op_desicion
                    last_opponent_for_second = f_op_decision

                    first_opponent_score += W[f_op_decision][sec_op_desicion]
                selection.append(first_opponent_score)

            middle_value = sum(selection) / len(selection)
            middle_values.append(middle_value)
            dispersi_values.append(count_dispersi(selection, middle_value))
            median_values.append(count_median(selection))
            mode_values.append(count_moda(selection))

        middle_values_result.append([first_parti] + middle_values)
        dispersi_values_result.append([first_parti] + dispersi_values)
        median_values_result.append([first_parti] + median_values)
        moda_values_result.append([first_parti] + mode_values)


    all_mid_score_by_strategies = []
    for res in middle_values_result:
        mid_all = 0
        for i in range(1, len(res)):
            mid_all += res[i]
        all_mid_score_by_strategies.append([res[0], mid_all / (len(res) - 1)])
    all_mid_score_by_strategies.sort(key = lambda x: x[1], reverse = True)

    with open("lab3_results.txt", "w") as out_file:
        out_file.write("Средние очки по стратегиям (среднее по всем соперникам)" + "\n")

        headers = ["Стратегия", "Среднее"]
        out_file.write(tabulate(all_mid_score_by_strategies, headers=headers, tablefmt="grid") + "\n" + "\n")

        out_file.write("Матрица средних очков (A против B)" + "\n")

        headers = ["Стратегия"] + part_keys
        out_file.write(tabulate(middle_values_result, headers = headers, tablefmt="grid") + "\n" + "\n")

        out_file.write("Матрица дисперсий (A против B)" + "\n")

        headers = ["Стратегия"] + part_keys
        out_file.write(tabulate(dispersi_values_result, headers=headers, tablefmt="grid") + "\n" + "\n")

        out_file.write("Матрица медианных очков (A против B)" + "\n")

        headers = ["Стратегия"] + part_keys
        out_file.write(tabulate(median_values_result, headers=headers, tablefmt="grid") + "\n" + "\n")

        out_file.write("Матрица моды (оценка по интервалам) (A против B)" + "\n")

        headers = ["Стратегия"] + part_keys
        out_file.write(tabulate(moda_values_result, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    main()