import textwrap


class Shoe:
    """Defines a shoe product that will be stored in a list."""
    # Constructor
    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity

    # Getters
    def get_cost(self):
        return self.cost

    def get_quantity(self):
        return self.quantity

    # Setter
    def set_quantity(self, amount):
        self.quantity = amount

    # Override str method to display formatted object details
    def __str__(self):
        return textwrap.dedent(f"Country:   {self.country}\n"
                               f"Code:      {self.code}\n"
                               f"Product:   {self.product}\n"
                               f"Cost:      {self.cost}\n"
                               f"Quantity:  {self.quantity}\n")
