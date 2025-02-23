import string

SPECIAL_SYMBOLS = "!@#$%&*+"


def remove_matching_characters(chars_to_remove: str, input_str: str):
    found_match = False
    for input_char in input_str:
        # лишний цикл убираем
        # for char_to_remove in chars_to_remove:
        #     if input_char == char_to_remove:
        #         found_match = True
        #         input_str = input_str.replace(char_to_remove, "")
        if input_char in chars_to_remove:
            found_match = True
            input_str = input_str.replace(input_char, "")
    return found_match, input_str


def is_valid_password(input_password: str) -> bool:
    is_valid = True
    if len(input_password) < 12:
        is_valid = False
    if is_valid:
        is_valid, input_password = remove_matching_characters(
            string.ascii_uppercase, input_password
        )
    if is_valid:
        is_valid, input_password = remove_matching_characters(
            string.ascii_lowercase, input_password
        )
    if is_valid:
        is_valid, input_password = remove_matching_characters(
            SPECIAL_SYMBOLS, input_password
        )
    if is_valid:
        is_valid, input_password = remove_matching_characters(
            string.digits, input_password
        )
    if len(input_password) > 0:
        is_valid = False
    return is_valid


if __name__ == "__main__":
    while True:
        try:
            n = int(input("Введите количество паролей: "))
            break
        except ValueError:
            print("Введено не число. Повторите ввод:")

    for _ in range(n):
        input_string = input("Введите пароль: ")
        if is_valid_password(input_string):
            print("Valid")
        else:
            print("Invalid")
