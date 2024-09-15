from snowfakery import SnowfakeryPlugin
from string import ascii_lowercase, ascii_uppercase, digits
from random import choice, randrange


class RandomString(SnowfakeryPlugin):
    class Functions:
        def random_string(self, length: int, fixed: bool, case: str) -> str:
            if fixed:
                max_length = length
            else:
                max_length = randrange(length)

            match case.upper():
                case 'UPPER':
                    randomString = ''.join(
                        [choice(ascii_uppercase) for i in range(max_length)])
                case 'LOWER':
                    randomString = ''.join(
                        [choice(ascii_lowercase) for i in range(max_length)])
                case 'NUMBERS':
                    randomString = ''.join(
                        [choice(digits) for i in range(max_length)])
                case 'CAPITALISE':
                    randomString = ''.join(
                        [choice(ascii_lowercase) for i in range(max_length)]).capitalize()
                case _:
                    randomString = ''.join(
                        [choice(ascii_lowercase) for i in range(max_length)]).capitalize()

            return randomString
