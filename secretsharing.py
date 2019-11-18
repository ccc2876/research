import time
import random


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


class SmartMeter:
    """
    attributes for Smart Meter class
    ID -- the ID that corresponds to each smart meter
    degree -- the number of aggregators -1, corresponds to degree of polynomial
    secret -- the secret that the smart meter has, updated at each time instance
    polynomial -- the randomly generated polynomial for creating shares
    coeff_list -- the randomly generated coefficients  used to create the polynomial
    shares_list -- holds the shares that this smart meter created
    """

    def __init__(self, ID, degree):
        self.ID = ID
        self.degree = degree
        self.secret = 0
        self.polynomial = ""
        self.coeff_list = []
        self.shares_list = []

    def set_polynomial(self, poly):
        """
        was used for testing of a predetermined polynomial
        :param poly:  the set polynomial of the smart meter
        """
        self.polynomial = poly

    def set_coeff_list(self, list):
        """
        was used for testing of a predetermined polynomial
        :param list: the coefficients of the polynomial
        """
        self.coeff_list = list

    def get_ID(self):
        """
        :return:  the ID of this smart meter
        """
        return self.ID

    def get_polynomial(self):
        """
        :return: the polynomial of this smart meter
        """
        return self.polynomial

    def set_secret(self, secret):
        """
        was used for a predetermined secret for testing purposes
        :param secret: the secret of the smart meter
        """
        self.secret = secret

    def create_polynomial(self):
        """
        function to create a polynomial at each time instance for a smart meter
        creates a random string of bits to determine the powers of x in the polynomial
        then generates a random integer as the coefficient for the bits that are 1s
        appends the secret to the end of the coefficient
        """
        self.coeff_list = []
        bit_string = [1]
        # loop over the range of the degree to generate whether the power of x will be present
        for i in range(1, self.degree):
            bit = random.randint(0, 1)
            bit_string.append(bit)
        power = self.degree
        polystring = ""

        # loop over the binary string and generate the coefficients
        for i in range(0, len(bit_string)):
            if bit_string[i] == 1:
                coeff = random.randint(1, 10)
                polystring += str(coeff) + "x^" + str(power) + "+"
                self.coeff_list.append(coeff)
            else:
                self.coeff_list.append(0)
            power -= 1

        # add the secret to the end of the polynomial as the constant
        polystring += str(self.secret)
        self.polynomial = polystring

    def create_shares(self, aggregator):
        """
        generates the shares from this smart meter
        using the polynomial that belongs to this smart meter the ID value of the aggregator that is passed in
        is plugged in for the x value and the share is the total of the polynomial
        appends the share value to the aggregator list and to the smart meter list
        :param aggregator: the aggregator that this share is being sent to
        """
        length = len(self.coeff_list)

        power = self.degree
        value = 0
        for i in range(0, length):
            value += self.coeff_list[i] * (aggregator.get_ID() ** power)
            power -= 1
        value += self.secret
        self.shares_list.append(value)

        if len(aggregator.shares_list) == self.ID - 1:
            aggregator.shares_list.append(value)
        else:
            aggregator.shares_list[self.ID - 1] += value

    def get_shares_list(self):
        return str(self.shares_list)


def main():
    # initializes the electrical utility
    eu = ElectricalUtility()

    # opens the file which contains the time instance, aggregator, and smart meter numbers
    f = open("data_input.txt")

    for line in f:
        line = line.split(",")
        time_instances = int(line[0])
        aggregators = int(line[1])
        sm_num = int(line[2])
        if time_instances < 1 or aggregators < 1 or sm_num <1:
            print("invalid input file, please retry")
            exit(1)

    out = open("outputfiles/case3/Case3" + "T" + str(time_instances) + "A" + str(aggregators) + "S" + str(sm_num) + ".txt", "w")

    aggregator_list = []
    smart_meter_list = []

    # generates polynomial degree based on number of aggregators
    degree = aggregators - 1

    for i in range(0, sm_num):
        # creates a smart meter with ID and degree and appends it to the list
        smart_meter = SmartMeter(i + 1, degree)
        smart_meter_list.append(smart_meter)

    for i in range(0, aggregators):
        # creates an aggregator with ID and appends it to the list and calculates lagrange value
        aggregator = Aggregator(i + 1)
        aggregator_list.append(aggregator)
        aggregator.calculate_lagrange_multiplier(aggregators)

    # begin loop on the number of time instances given
    for t in range(0, time_instances):
        out.write("Time instance " + str(t) + "\n\n")

        # generate a random number as the secret for the smart meter
        for i in range(0, sm_num):
            secret = random.randint(1, 5)
            smart_meter_list[i].set_secret(secret)  # eventually will come from other data
            out.write("Secret for Smart Meter #" + str(i) + ": " + str(secret) + "\n")

        # create each smart meters polynomial
        for meter in smart_meter_list:
            meter.create_polynomial()

        # start the timer for sending shares
        start = time.time()
        # create each share
        for sm in smart_meter_list:
            for aggregator in aggregator_list:
                sm.create_shares(aggregator)

        # update the aggregator totals
        for agg in aggregator_list:
            agg.update_totals()

        # end the timer and print elapsed time
        end = time.time()
        out.write("Elapsed time: " + str(end - start) + "\n\n")

        # print out the smart meter polynomial, the aggregator shares list, and the totals
        for sm in smart_meter_list:
            out.write("Polynomial for Smart Meter #" + str(sm.get_ID()) + ": " + sm.get_polynomial() + "\n")
            out.write("Shares for Smart Meter #" + str(sm.get_ID()) + ": " + sm.get_shares_list() + "\n")
            out.write("\n")

        for a in aggregator_list:
            out.write("Shares list for aggregator #" + str(a.get_ID()) + ": " + a.print_shares_list() + "\n")
            out.write("Total of Aggregator #" + str(a.get_ID()) + ": " + str(a.total) + "\n")
            out.write("Current total of Aggregator #" + str(a.get_ID()) + ": " + str(a.current_total) + "\n")
            out.write("\n")

        # calculate the values to be shared between smart meters for reconstruction of the secrets
        constants = []
        for a in aggregator_list:
            constant = a.get_current_total() * a.get_lagrange_multiplier()
            constants.append(constant)

        # send the data to the electric utility company
        eu.add_reading(abs(sum(constants)))
        for e in eu.return_values():
            out.write(str(e) + "\n")
        out.write("\n")

        # close the file
        out.close
        f.close()


main()
