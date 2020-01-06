import random
import socket
import pickle
import time


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

    def __init__(self):
        self.ID = 0
        self.degree = 0
        self.secret = 0
        self.polynomial = ""
        self.coeff_list = []
        self.shares_list = []
        self.times_list = []

    def set_id(self, ID):
        self.ID = ID

    def set_degree(self, deg):
        self.degree = deg

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
        print(self.polynomial)

    def create_shares(self, aggregator_ID):
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
            value += self.coeff_list[i] * (aggregator_ID ** power)
            power -= 1
        value += self.secret
        self.shares_list.append(value)
        return value

    def get_shares_list(self):
        return str(self.shares_list)

    def add_time(self, value):
        self.times_list.append(value)

    def get_time(self):
        print(self.times_list)


# if __name__ == '__main__':
#     TCP_IP = '127.0.0.1'
#     TCP_PORT1 = 5006
#     TCP_PORT2 = 5007
#     BUFFER_SIZE = 1024
#     connections = []
#     s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     s1.connect((TCP_IP, TCP_PORT1))
#     connections.append(s1)
#     s2.connect((TCP_IP, TCP_PORT2))
#     connections.append(s2)
#     t = 9
#     s1.send(pickle.dumps(t))
#     s2.send(pickle.dumps(t))
#     aggregator_IDs = []
#     d1 = s1.recv(1024)
#     d2 = s2.recv(1024)
#     d1 = pickle.loads(d1)
#     d2 = pickle.loads(d2)
#     aggregator_IDs.append(d1)
#     aggregator_IDs.append(d2)
#     data = pickle.dumps(aggregator_IDs)
#     s1.send(data)
#     s2.send(data)
#     secrets = []
#
#     for t in range(0, 9):
#         print("Time Instance #", t)
#         constants = []
#         secret = random.randint(1, 5)
#         sm = SmartMeter()
#         sm.set_id(1)
#         sm.set_degree(len(aggregator_IDs) - 1)
#         sm.set_secret(secret)
#         secrets.append(secret)
#         sm.create_polynomial()
#         counter = 0
#         shares = []
#         for id in aggregator_IDs:
#             single_share_time_start = time.time()
#             val = sm.create_shares(id)
#             shares.append(val)
#             connections[counter].send(pickle.dumps(val))
#             single_share_time_end = time.time()
#             sm.add_time(single_share_time_end - single_share_time_start)
#             print(single_share_time_end - single_share_time_start)
#             counter += 1
#         print("Shares for smart meter: ", shares)
#     print(sum(secrets))
#
#     for conn in connections:
#         conn.close()
#
