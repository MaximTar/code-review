def divide_numbers(a, b):
  result = a / b   # ❌ Possible division by zero
  return result

def greeting():
  print("Hello, world!")
  return 5  # ❌ Unused return value

print(divide_numbers(10, 2))
print(divide_numbers(5, 0))  # ❌ Runtime error

