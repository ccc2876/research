

class Aggregator:
    """
    Aggregator class attributes
    ID -- the ID that corresponds to the aggregators
    shares_list -- the list of shares that the smart meters send to the aggregator
        gets added to as more shares come from the same smart meters
    total -- the total of all the shares added together
    current_total -- the total of the most recent shares
    delta_func_multiplier -- the delta function multiplier which is made using lagrange interpolation
    """

    def __init__(self, ID):
        self.ID = ID
        self.shares_list = []
        self.current_total = 0
        self.total = 0
        self.delta_func_multiplier = 0
        self.lagrange = ""

    def set_lagrange(self, equation):
        self.lagrange = equation

    def calculate_lagrange_multiplier(self, num_aggregators):
        """
        utilizes the idea of lagrange interpolation to create a multiplier for the recreation of the secrets
        :param num_aggregators: the total number of aggregators that are in the system
        """
        top = 1
        bottom = 1
        for i in range(1, num_aggregators + 1):
            if i != self.get_ID():
                top *= i
                bottom *= (self.get_ID() - i)

        self.delta_func_multiplier = top / bottom

    def print_shares_list(self):
        """
        :return: a string of the list of shares that the aggregator has received
        """
        shares = ""
        for s in self.shares_list:
            shares += str(s)
            shares += " "
        return shares

    def get_ID(self):
        """
        :return: the ID of the aggregator
        """
        return self.ID

    def update_totals(self):
        """
        updates the totals that the aggregator holds
        total is the total combined shares from all time instances and aggregators
        current total is the total from the most recent set of shares
        """
        temp = self.total
        self.total = sum(self.shares_list)
        self.current_total = self.total - temp

    def get_current_total(self):
        """
        :return: the current total of the shares that were most recently sent
        """
        return self.current_total

    def get_lagrange_multiplier(self):
        """
        :return: the lagrange multiplier
        """
        return self.delta_func_multiplier
