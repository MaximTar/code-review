def compress_message(msg: str) -> str:
    output_string = ""
    counter = 1
    for i in range(0, len(msg) - 1):
        if msg[i] == msg[i + 1]:
            counter += 1
        elif counter == 1:
            output_string += msg[i]
        else:
            # fixme NIT output_string += str(counter) + msg[i]
            output_string += f"{counter}{msg[i]}"
            counter = 1

    if counter > 1:
        # fixme NIT аналогично: output_string += str(counter) + msg[-1]
        output_string += f"{counter}{msg[-1]}"
    else:
        output_string += msg[-1]

    return output_string


if __name__ == "__main__":
    input_string = input("Введите сообщение: ")
    print("Сжатое сообщение", compress_message(input_string))
