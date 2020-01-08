class ElectricalUtility:
    """
    class for the electrical utility company
    includes a list of the values that the EU is sent at each time instance
    these values are comprised of the total of the secrets from the smart meters
    """

    def __init__(self):
        self.values = []
        self.num_aggregators = 0
        self.smart_meter_num = 0

    def set_num_aggs(self, num):
        self.num_aggregators = num

    def set_num_sm(self, num):
        self.smart_meter_num = num
        self.values = [0] * self.smart_meter_num

    def add_sums(self, x, sm_id):
        self.values[int(sm_id) - 1] += x

    def return_values(self):
        """
        prints the list of values
        """
        return self.values
