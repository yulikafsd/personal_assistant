class ValidationError(Exception):
    def __init__(self, message):
        self.message = f'\n{"-"*5} {message} {"-"*5}'
        super().__init__(self.message)
