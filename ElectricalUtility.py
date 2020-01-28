__author__ = "Claire Casalnova"


class ElectricalUtility:
    """
    class for the electrical utility company
    includes a list of the values that the EU is sent at each time instance
    these values are comprised of the total of the secrets from the smart meters
    """

    def __init__(self):
        """
        values- corresponds to the readings from specified smart meters
        num_aggregators - the number of aggregators in the network
        smart_meter_num - the number of smart meters in the network
        """
        self.value = 0
        self.num_aggregators = 0
        self.smart_meter_num = 0

    def set_num_aggs(self, num):
        """
        sets the num_aggregators in the network
        :param num: the number of aggs
        """
        self.num_aggregators = num

    def set_num_sm(self, num):
        """
        set the number of smart meters var and create the values array to be that length
        :param num: number of smart meters
        """
        self.smart_meter_num = num


    def add_sums(self, x):
        """
        append the reading to the correct location in the array
        :param x: the reading from the aggregators
        :param sm_id: the smart meter that the reading comes from
        """
        print("value:", self.value, "x:", x)
        self.value += x

    def return_values(self):
        """
        prints the list of values
        """
        return self.value
