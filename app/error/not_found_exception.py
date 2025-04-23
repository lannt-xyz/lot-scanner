class NotFoundException(Exception):
    def __init__(self):
        self.message = "Request not found."
        super().__init__(self.message)
