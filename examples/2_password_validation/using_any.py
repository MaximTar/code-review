def is_contain_lowercase(string: str) -> bool:
    return any(char.islower() for char in string)


def is_contain_uppercase(string: str) -> bool:
    return any(char.isupper() for char in string)


def is_contain_digit(string: str) -> bool:
    return any(char.isdigit() for char in string)


def is_contain_symbol(string: str) -> bool:
    return any(char in "!@#$%&*+" for char in string)


def is_valid_password(password: str) -> bool:
    if len(password) < 12:
        return False
    return (
        is_contain_lowercase(password)
        and is_contain_uppercase(password)
        and is_contain_digit(password)
        and is_contain_symbol(password)
    )


if __name__ == "__main__":
    n = int(input("Введите количество паролей: "))
    for _ in range(n):
        password_to_check = input("Введите пароль: ")
        print("Valid" if is_valid_password(password_to_check) else "Invalid")
