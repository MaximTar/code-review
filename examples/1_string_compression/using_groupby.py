from itertools import groupby


def compress_message(msg: str) -> str:
    return "".join(
        f"{length}{char}" if (length := len(list(group))) > 1 else char
        for char, group in groupby(msg)
    )


if __name__ == "__main__":
    message = input("Введите сообщение: ")
    print("Сжатое сообщение:", compress_message(message))
