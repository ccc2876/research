class ElectricalUtility:
    """
    class for the electrical utility company
    includes a list of the values that the EU is sent at each time instance
    these values are comprised of the total of the secrets from the smart meteres
    """

    def __init__(self):
        self.values = []

    def add_reading(self, value):
        """
        adds a new value to the list
        :param value: the total consumption from all of the smart meters combined
        """
        self.values.append(value)

    def return_values(self):
        """
        prints the list of values
        """
        return self.values

