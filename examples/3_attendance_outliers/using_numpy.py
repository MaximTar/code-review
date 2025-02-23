import numpy as np


def detect_outliers(attendance: list) -> int:
    attendance.sort()
    q1, q3 = np.percentile(attendance, [25, 75])
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    return sum(1 for x in attendance if x < lower_bound or x > upper_bound)


n = int(input("Введите количество пар: "))
attendance_data = [
    int(input(f"Количество студентов на {i + 1} паре: ")) for i in range(n)
]
print(
    f"Количество отмеченных пар, которые можно считать некорректными: "
    f"{detect_outliers(attendance_data)}"
)
