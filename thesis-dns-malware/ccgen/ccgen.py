"""
Based on: https://github.com/bizdak/ccgen
"""
import random
import string

import faker
from faker.providers.credit_card import Provider

_fake = faker.Faker()
_vendors = ['visa16', 'visa19', 'mastercard']


def gen_card(track: int):
    # Select random card vendor
    vendor = random.choice(_vendors)
    card = Provider.credit_card_types[vendor]

    # Gather card information
    owner = f"{_fake.first_name()}/{_fake.last_name()}".upper()
    number = _fake.credit_card_number(card)
    expires = _fake.credit_card_expire(date_format='%m%y')

    # Generate secrets
    service_code = ''.join(random.choices(string.digits, k=3))
    pvv = ''.join(random.choices(string.digits, k=4))

    if track == 1:

        # Max length of data is 77, plus B prefix and ? postfix == 79

        # Owner is max 28 chars
        owner = owner[:28]

        # Optionally pad with spaces
        if _fake.boolean():
            owner = f"{owner:28}"

        t1 = f"{number}^{owner}^{expires}{service_code}"

        # Add random amount of discretionary data (max 35 chars)
        dd_len = min(77 - len(t1), _fake.random_int(0, 35))
        return f"B{t1}{_fake.random_number(dd_len)}?"

    elif track == 2:

        # Max length of data is 36, plus ; prefix, = in the middle and ?3 postfix == 40
        if vendor == "visa16" or vendor == "visa19":
            t2 = f"{number}={expires}{service_code}{pvv}"

            # Append random discretionary data
            return f";{t2}{_fake.random_number(37 - len(t2))}?8"

        elif vendor == "mastercard":
            t2 = f"{number}={expires}{service_code}"

            # Append random discretionary data
            return f";{t2}{_fake.random_number(37 - len(t2))}?3"

    # Raise error for invalid configurations
    raise NotImplementedError()


class CreditCardGenerator:
    """Generator which produces either track 1 or track 2 credit card details."""

    def __init__(self, track_type: int = None, limit: int = None):
        self.remaining = limit
        self.track_type = track_type

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        ttype = random.choice((1, 2)) if not self.track_type else self.track_type

        if self.remaining is None:
            return gen_card(ttype), ttype

        if self.remaining > 0:
            self.remaining -= 1
            return gen_card(ttype), ttype
        else:
            raise StopIteration()


# Smoke test
if __name__ == "__main__":
    # Unlimited t1/t2
    unlimited_cards = CreditCardGenerator()
    print(next(unlimited_cards))

    # Specify track
    t1_cards = CreditCardGenerator(track_type=1)
    print(next(t1_cards))

    t2_cards = CreditCardGenerator(track_type=2)
    print(next(t2_cards))

    # Limit generator
    limited_cards = CreditCardGenerator(limit=1)
    print(next(limited_cards))
    print(next(limited_cards))  # raises StopIteration()

