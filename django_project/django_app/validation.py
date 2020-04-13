import re


class Validation:

    def username_validate(self, username):
        # This function is used to check username is in valid format or not and return true or false value
        if re.match(r"(^[a-zA-Z][a-zA-Z0-9_-]{3,16}$)", username):
            return True
        return False

    def email_validate(self, email):
        # This function is used to check email is in valid format or not and return true or false value
        if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            return True
        return False

    def password_validate(self, password):
        # This function is used to check psw is in valid format or not and return true and false value
        if re.match(r"([A-Za-z0-9@#$%^&+=]{8,})", password):
            return True
        return False
