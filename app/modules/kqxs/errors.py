class IncorrectResultException(Exception):
    def __init__(self):
        self.message = "Craw result is incorect."
        super().__init__(self.message)

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
