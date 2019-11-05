import random
from sys import maxsize


class Aggregator:
    def __init__(self, ID):
        self.ID = ID
        self.shares_list = []
        self.running_total = 0
        self.current_total = 0

    def get_ID(self):
        return self.ID

    def print_shares_list(self):
        shares = ""
        for s in self.shares_list:
            shares += str(s)
            shares += ", "
        return shares


class SmartMeter:

    def __init__(self, degree, secret, ID):
        self.ID = ID
        self.degree = degree
        self.secret = secret
        self.polynomial = ""
        self.coeff_list = []
        self.bin_string =[]

    def get_ID(self):
        return self.ID

    def create_poly(self):
        # create a string of binary numbers for the x values
        self.bin_string.append(1)

        # loop over the range of the degree to generate whether the power of x will be present
        for i in range(1, self.degree):
            bit = random.randint(0, 1)
            self.bin_string.append(bit)
        power = self.degree
        polystring = ""

        # loop over the binary string and generate the coefficients
        for i in range(0, len(self.bin_string)):
            if self.bin_string[i] == 1:
                coeff = random.randint(1, maxsize)
                polystring += str(coeff) + "x^" + str(power) + "+"
                self.coeff_list.append(coeff)
            else:
                self.coeff_list.append(0)
            power -= 1

        # add the secret to the end of the polynomial as the constant
        polystring += str(self.secret)
        self.polynomial = polystring

    def create_shares(self, agg):
        length = len(self.coeff_list)
        power = self.degree

        value = 0

        for i in range(0, len(self.bin_string)):
            if self.bin_string[i] != 0:
                value += self.coeff_list[i] * (agg.get_ID() ** power)
            power -= 1

        value += self.secret
        agg.shares_list.append(value)

    def get_poly(self):
        return self.polynomial


def get_aggs():
    # ask for number of aggregators
    aggregators = int(input("How many aggregators? "))
    while aggregators < 1:
        aggregators = int(input("How many aggregators? "))

    return aggregators


def get_smart_meters():
    sm = int(input("How many smart meters? "))
    while sm < 1:
        sm = int(input("How many smart meters? "))
    return sm


def main():
    aggregator_list = []
    smart_meter_list = []

    aggregators = get_aggs()
    degree = aggregators - 1

    for i in range(1, aggregators + 1):
        a = Aggregator(i)
        aggregator_list.append(a)

    sm_num = get_smart_meters()
    for i in range(1, sm_num + 1):
        secret = int(input("What is the secret for Smart Meter #" + str(i) + "? "))
        while secret < 1:
            secret = int(input("What is the secret for Smart Meter #" + str(i) + "? "))

        sm = SmartMeter(degree, secret, i)
        smart_meter_list.append(sm)

    for sm in smart_meter_list:
        sm.create_poly()

    for sm in smart_meter_list:
        for agg in aggregator_list:
            sm.create_shares(agg)

    print()

    for sm in smart_meter_list:
        print("Polynomial for Smart Meter #" + str(sm.get_ID()) + ": " + sm.get_poly())

    print()

    for a in aggregator_list:
        print("Shares list for aggregator #" + str(a.get_ID()) + ": " + a.print_shares_list())


main()
