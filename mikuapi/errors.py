# mikuapi/errors.py

class ValidationError(Exception):
    def __init__(self, message):
        self.message = message