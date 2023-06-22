from dotenv import dotenv_values

# Load environment variables from .env file
ENV = dotenv_values('.env')
DEBUG = ENV.get('DEBUG', 'False') == 'True'


def is_debug() -> bool:
    return DEBUG


def debug(texto: str, espacador: bool = False):
    if DEBUG:
        print(texto if espacador else '\n')
