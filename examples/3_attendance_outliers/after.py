import math


def get_integer_input(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Введено не число. Повторите ввод")


def get_attendances(counter: int) -> list[int]:
    return [
        get_integer_input(f"Введите посещаемость на {i + 1} паре: ")
        for i in range(counter)
    ]


def calculate_median(lst: list[int]):
    length = len(lst)
    mid = length // 2
    if length % 2 == 0:
        return (lst[mid] + lst[mid - 1]) / 2
    else:
        return lst[mid]


def calculate_outliers(input_list: list[int]) -> int:
    input_list.sort()
    length = len(input_list)
    first_half = input_list[: length // 2]
    second_half = input_list[math.ceil(length / 2) :]
    first_quartile = calculate_median(first_half)
    third_quartile = calculate_median(second_half)
    iqr = third_quartile - first_quartile
    lower_bound = first_quartile - 1.5 * iqr
    upper_bound = third_quartile + 1.5 * iqr

    # fixme можно немного сократить
    # outlier_count = 0
    # for element in input_list:
    #     if element < lower_bound or element > upper_bound:
    #         outlier_count += 1

    return sum(1 for x in input_list if x < lower_bound or x > upper_bound)


if __name__ == "__main__":
    pair_count = get_integer_input(
        "Введите количество пар, на которых отмечалась посещаемость: "
    )
    attendances = get_attendances(pair_count)
    print(
        f"Количество отмеченных пар, которые можно считать некорректными: "
        f"{calculate_outliers(attendances)}"
    )
