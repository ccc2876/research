import random
from sys import maxsize
import copy
import time


class Aggregator:
    """
    Aggregator class attributes
    ID -- the ID that corresponds to the aggregators
    shares_list -- the list of shares that the smart meters send to the aggregator
        gets added to as more shares come from the same smart meters
    running_total -- the total of all the shares added together
    current_total -- the total of the most recent shares
    delta_func -- the delta function made from the IDs of all the aggregators
    """

    def __init__(self, ID):
        self.ID = ID
        self.shares_list = []
        self.running_total = 0
        self.current_total = 0
        self.delta_func = ""

    def get_ID(self):
        """
        :return: the ID of the aggregator
        """
        return self.ID

    def print_shares_list(self):
        """
        :return: a string of the list of shares that the aggregator has received
        """
        shares = ""
        for s in self.shares_list:
            shares += str(s)
            shares += " "
        return shares

    def make_delta(self, delta):
        """
        sets the delta function sent as the delta function of the aggregator
        :param delta: the delta function for the aggregator
        """
        self.delta_func = delta
        return self.delta_func

    def update_totals(self):
        """
        calculates the current and running totals of the shares
        """

        self.running_total = sum(self.shares_list)
        self.current_total = self.running_total - self.current_total


class SmartMeter:
    """

    """
    def __init__(self, degree, ID):
        self.ID = ID
        self.degree = degree
        self.secret = 0
        self.polynomial = ""
        self.coeff_list = []

    def set_secret(self, secret):
        """
        gets the secret input
        :param secret: the utility consumption amount
        """
        self.secret = secret

    def get_ID(self):
        """
        :return: the ID of the smart meter
        """
        return self.ID

    def create_poly(self):
        """
        create the polynomial to create shares
        """

        bin_string = [1]

        # loop over the range of the degree to generate whether the power of x will be present
        for i in range(1, self.degree):
            bit = random.randint(0, 1)
            bin_string.append(bit)
        power = self.degree
        polystring = ""

        # loop over the binary string and generate the coefficients
        for i in range(0, len(bin_string)):
            if bin_string[i] == 1:
                coeff = random.randint(1, 10)
                polystring += str(coeff) + "x^" + str(power) + "+"
                self.coeff_list.append(coeff)
            else:
                self.coeff_list.append(0)
            power -= 1

        # add the secret to the end of the polynomial as the constant
        polystring += str(self.secret)
        self.polynomial = polystring

    def create_shares(self, agg):
        """
        create the shares based on the ID of the aggregator
        :param agg: aggregator that the share is being sent to
        """
        length = len(self.coeff_list)
        power = length
        value = 0

        for i in range(0, length):
            value += self.coeff_list[i] * (agg.get_ID() ** power)
            power -= 1
        value += self.secret
        if len(agg.shares_list) == self.ID - 1:
            agg.shares_list.append(value)
        else:
            agg.shares_list[self.ID - 1] += value

    def get_poly(self):
        """
        :return: the polynomial of the smart meter
        """
        return self.polynomial


def get_aggs():
    """
    ask for number of aggregators
    """
    aggregators = int(input("How many aggregators? "))
    while aggregators < 1:
        aggregators = int(input("How many aggregators? "))

    return aggregators


def get_smart_meters():
    """
       ask for number of smart meters
       """
    sm = int(input("How many smart meters? "))
    while sm < 1:
        sm = int(input("How many smart meters? "))
    return sm


def get_time_instances():
    """
       ask for number of time instances
       """
    time_instances = int(input("How many time instances? "))
    while time_instances < 1:
        time_instances = int(input("How many time instances? "))
    return time_instances


def main():
    ti = get_time_instances()
    aggregator_list = []
    smart_meter_list = []

    aggregators = get_aggs()
    degree = aggregators - 1

    sm_num = get_smart_meters()
    for i in range(1, sm_num + 1):
        sm = SmartMeter(degree, i)
        smart_meter_list.append(sm)

    for i in range(1, aggregators + 1):
        a = Aggregator(i)
        aggregator_list.append(a)

    for t in range(0, ti):
        for i in range(1, sm_num + 1):
            secret = int(input("What is the secret for Smart Meter #" + str(i) + "? "))
            while secret < 1:
                secret = int(input("What is the secret for Smart Meter #" + str(i) + "? "))
            smart_meter_list[i - 1].set_secret(secret)

        for sm in smart_meter_list:
            sm.create_poly()
        start = time.time()

        for sm in smart_meter_list:
            for agg in aggregator_list:
                sm.create_shares(agg)

        for agg in aggregator_list:
            agg.update_totals()

        end = time.time()
        print()
        print("Time Elapsed: ", end - start)

        for sm in smart_meter_list:
            print("Polynomial for Smart Meter #" + str(sm.get_ID()) + ": " + sm.get_poly())

        print()

        for a in aggregator_list:
            print("Shares list for aggregator #" + str(a.get_ID()) + ": " + a.print_shares_list())
            print("Running total of Aggregator #", a.get_ID(), a.running_total)
            print("Current total of Aggregator #", a.get_ID(), a.current_total)

        agg_list2 = copy.deepcopy(aggregator_list)

        for i in range(0, len(agg_list2)):
            a = agg_list2.pop(0)
            top = ""
            bottom = 1

            for a2 in agg_list2:
                top += "(x - " + str(a2.get_ID()) + ")"
                bottom *= (a.get_ID() - a2.get_ID())
                print("Delta function for aggregator #", a.get_ID(), a.make_delta(top + " / " + str(bottom)))

            agg_list2.append(a)
        print()

"""
2 lists in the aggregator 
1 counter in the smart meter 
"""

main()
