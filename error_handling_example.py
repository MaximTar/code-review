import time


def run_server_bad():
    try:
        while True:
            print("Server running...")
            time.sleep(2)  # Имитация активности сервера
            raise MemoryError  # Имитация отсутствия памяти
    except Exception:
        print("Error occurred! Restarting server...")
        run_server_bad()  # Никогда не остановится, даже при фатальных ошибках


def run_server_better():
    try:
        while True:
            print("Server running...")
            time.sleep(2)
            raise MemoryError  # Имитация отсутствия памяти
    except MemoryError as e:
        print(f"Critical error: {e}. Shutting down gracefully.")
        raise  # Повторный вызов системной ошибки, чтобы остановить выполнение
    except Exception as e:
        print(f"Unexpected error: {e}. Restarting server...")
        run_server_better()  # Перезапуск только при некритических ошибках


if __name__ == "__main__":
    run_server_bad()
    # run_server_better()
