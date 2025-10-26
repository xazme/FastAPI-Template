from pathlib import Path

ROOT_DIR = Path(__file__).parents[
    2
]  # спускаемся на 2 уровня ниже относительно этого файла
APP_DIR = ROOT_DIR.joinpath("app")  # добавляем к пути папку исходников проекта
ENV_FILE_PATH = ROOT_DIR.joinpath(".env")  # добавляем путь до env файла

print(ROOT_DIR)
print(ENV_FILE_PATH)
