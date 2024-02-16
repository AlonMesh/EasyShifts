import re


class AuthenticationUser:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __validate_username(self):
        """
            Check if username is in English with no spaces and other criteria
        Args:
            username: The username to validate

        Returns: True if valid, False otherwise
        """
        # Define a regular expression pattern for English letters only
        english_letters_and_digits_pattern = re.compile(r'^[a-zA-Z0-9]+$')

        # Check if the username contains only English letters and no spaces
        if not english_letters_and_digits_pattern.match(self.username) or ' ' in self.username:
            return False

        return True

    def __fun2(self):
        pass

    def login(self, username, password):
        if not self.__validate_username():
            raise ValueError("Invalid username")

        pass
