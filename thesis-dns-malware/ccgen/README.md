# Thesis - Credit Card Generator
Python library to generate track1 or track2 credit card details. Uses [Faker](https://faker.readthedocs.io/en/master/) to generate "real" credit card details and account holder names. Randomly selects one of `['visa16', 'visa19', 'mastercard']` formats.

Used in thesis to simulate PoS-malware data exfiltration over DNS.

## Usage
```python
import CreditCardGenerator

# Unlimited t1/t2
unlimited_cards = CreditCardGenerator()

print(next(unlimited_cards))
# ('B4606041507791402^ERICA/BOOTH^0131085791886390496855463?', 1)

# Specify track
t1_cards = CreditCardGenerator(track_type=1)

print(next(t1_cards))
# ('B2280419368409990^SARAH/SMITH^10288247077299949788162601358395407?', 1)

t2_cards = CreditCardGenerator(track_type=2)
print(next(t2_cards))
# (';4873311911523264438=0424069385587597?8', 2)

# Limit number of cards
limited_cards = CreditCardGenerator(limit=1)
print(next(limited_cards))  # (';4384421501173120=10252192066125296205?8', 2)
print(next(limited_cards))  # raises StopIteration()
```
