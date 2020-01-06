from _thread import *
import socket
import pickle
from numpy import long
import sys


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

    def __init__(self, ID, num_smart_meters):
        self.ID = ID
        self.shares_list = [0] * num_smart_meters
        self.current_total = [0] * num_smart_meters
        self.total = [0] * num_smart_meters
        self.delta_func_multiplier = 0
        self.lagrange = ""
        self.sumofshares= [0] * num_smart_meters

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
                top *= -i
                bottom *= (self.get_ID() - i)
        self.delta_func_multiplier = top / bottom
        print(self.delta_func_multiplier)

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

    def update_totals(self, sm_id):
        """
        updates the totals that the aggregator holds
        total is the total combined shares from all time instances and aggregators
        current total is the total from the most recent set of shares
        """
        temp = self.total[sm_id-1]
        self.total[sm_id-1] = self.shares_list[sm_id-1]
        self.current_total[sm_id-1] = self.total[sm_id-1] - temp

    def get_current_total(self, sm_id):
        """
        :return: the current total of the shares that were most recently sent
        """
        return self.current_total[sm_id-1]

    def get_lagrange_multiplier(self):
        """
        :return: the lagrange multiplier
        """
        return self.delta_func_multiplier

    def append_shares(self, share, sm_id):
        # self.shares_list.append(share)
        # print(self.shares_list)
        self.shares_list[int(sm_id)-1] += share
        print(self.shares_list)

    def calc_sum(self,value, sm_id):
        self.sumofshares[sm_id-1] += value

    def get_sum(self, sm_id):
        return self.sumofshares[sm_id-1]


def threaded(conn, ag, client, t):
    agg = conn.recv(1024)
    if agg:
        agg = pickle.loads(agg)

        for j in range(0, len(agg)):
            agg[j] = int(agg[j])

        ag.calculate_lagrange_multiplier(len(agg))

        counter = 0
        while counter < t:
            data = conn.recv(1024)
            if data:
                data = pickle.loads(data)
                ag.append_shares(data)
                ag.update_totals()
                constant = long(ag.get_current_total()) * long(ag.get_lagrange_multiplier())
                ag.calc_sum(constant)
                counter += 1

        val = ag.get_sum()
        print(val)
        client.send(pickle.dumps(val))
        conn.close()


if __name__ == '__main__':
    # set up connection to the utility company
    TCP_IP = '127.0.0.1'
    TCP_PORT = int(sys.argv[1])
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((TCP_IP, TCP_PORT))

    # set up connection to the smart meters
    TCP_IP = '127.0.0.1'
    TCP_PORT = int(sys.argv[2])
    BUFFER_SIZE = 1024
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))

    smart_meter_list = []
    aggregator_list = []
    ID = int(sys.argv[3])
    aggregator = Aggregator(ID)
    aggregator_list.append(aggregator)

    lcounter = 0
    for i in range(0, len(aggregator_list)):
        a = aggregator_list[lcounter]
        top = ""
        bottom = 1
        for a2 in aggregator_list:
            if not a2.get_ID() == a.get_ID():
                top += "(x - " + str(a2.get_ID()) + ")"
                bottom *= (a.get_ID() - a2.get_ID())
                a.set_lagrange(top + "/" + str(bottom))
        lcounter += 1

    while True:
        s.listen()
        conn, addr = s.accept()
        print('Connected to :', addr[0], ':', addr[1])
        smart_meter_list.append(conn)
        conn.send(pickle.dumps(ID))
        t = conn.recv(1024)
        t = pickle.loads(t)
        print("time", t)
        start_new_thread(threaded, (conn, aggregator, client, t))


