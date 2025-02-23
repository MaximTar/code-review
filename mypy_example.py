def add_numbers_(a, b) -> int:  # no type hints
    return a + b

def add_numbers(a: int, b: int) -> int:
    return a + b

print(add_numbers_(10, "20"))  # TypeError not detected by mypy
print(add_numbers(10, "20"))  # TypeError detected by mypy
