def divide_numbers(a, b):
  result = a / b   # ❌ Возможное деление на ноль
  return result

print(divide_numbers(10, 2))
print(divide_numbers(5, 0))  # ❌ Runtime error

