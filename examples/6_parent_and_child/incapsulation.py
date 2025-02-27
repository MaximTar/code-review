class Config:
    def __init__(self):
        self.max_users = 100

    def set_max_users(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("max_users должно быть положительным целым числом")
        self.max_users = value


class Service:
    def __init__(self, config: Config):
        self.config = config

    def process_users(self, user_count):
        if user_count > self.config.max_users:
            print("Слишком много пользователей. Запрос отклонен")
        else:
            print(f"Обработка {user_count} пользователей...")


class ConfigManager:
    def __init__(self, config: Config):
        self.config = config

    def update_config(self):
        self.config.max_users = "unlimited"
        # self.config.set_max_users("unlimited")


cfg = Config()
service = Service(cfg)
config_manager = ConfigManager(cfg)
config_manager.update_config()
service.process_users(50)
