def add_numbers_(a, b) -> int:  # без тайп хинтов
    return a + b

def add_numbers(a: int, b: int) -> int:
    return a + b

print(add_numbers_(10, "20"))  # TypeError не обнаруженный mypy
print(add_numbers(10, "20"))  # TypeError обнаруженный mypy
