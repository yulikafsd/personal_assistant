from colorama import Fore, Style, init


class Colorize:
    # Клас для кольорового виводу тексту в консолі
    init()

    @staticmethod
    def colorize(text: str, color: str) -> str:
        color_dict = {
            "error": Fore.RED,
            "success": Fore.GREEN,
            "warning": Fore.YELLOW,
            "info": Fore.BLUE,
            "highlight": Fore.CYAN,
        }
        color_code = color_dict.get(color.lower(), Fore.RESET)
        return f"{color_code}{text}{Style.RESET_ALL}"

    @staticmethod
    # Статичні методи для різних типів повідомлень
    def error(message: str) -> str:
        return Colorize.colorize(message, "error")

    @staticmethod
    def success(message: str) -> str:
        return Colorize.colorize(message, "success")

    @staticmethod
    def warning(message: str) -> str:
        return Colorize.colorize(message, "warning")

    @staticmethod
    def info(message: str) -> str:
        return Colorize.colorize(message, "info")

    @staticmethod
    def highlight(message: str) -> str:
        return Colorize.colorize(message, "highlight")