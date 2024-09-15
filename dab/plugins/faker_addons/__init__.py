from random import choice, uniform
from faker.providers import BaseProvider

products = [
    'MacBook Pro',
    'MacBook Air',
    'iPhone',
    'iPad',
    'iPad Pro',
    'Apple Watch',
    'Apple TV',
    'AirTag',
    'HomePod',
    'iMac'
]


class Provider(BaseProvider):

    def yes_no(self) -> str:
        choices = ['Y', 'N']
        return choice(choices)

    def product(self) -> str:
        return choice(products)

    def amount(self) -> float:
        return round(uniform(333.00, 666.99), 2)

    def percentage(self) -> float:
        return round(uniform(0.00, 100.00), 2)
