import socket
from _thread import *
import threading
import pickle
import sys

print_lock = threading.Lock()


class ElectricalUtility:
    """
    class for the electrical utility company
    includes a list of the values that the EU is sent at each time instance
    these values are comprised of the total of the secrets from the smart meteres
    """

    def __init__(self):
        self.values = []
        self.sums = []
        self.reading = 0
        self.num_aggregators = 0
        self.counter = 0
        self.smart_meter_num =0

    def set_num_aggs(self, num):
        self.num_aggregators = num

    def set_num_sm(self, num):
        self.smart_meter_num = num
        self.values = [0] * self.smart_meter_num


    def add_reading(self, value):
        """
        adds a new value to the list
        :param value: the total consumption from all of the smart meters combined
        """
        self.values.append(value)

    def add_sums(self, x, sm_id):
        self.values[int(sm_id)-1] += x


    def return_values(self):
        """
        prints the list of values
        """
        return self.values


def threaded(conn, eu):
    data = conn.recv(1024)
    if not data:
        print(data)

    val = pickle.loads(data)
    eu.add_sums(val)


if __name__ == '__main__':
    eu = ElectricalUtility()
    TCP_IP = '127.0.0.1'
    PORT = int(sys.argv[1])
    BUFFER_SIZE = 1024
    connections = []
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, PORT))

    print("Server started")
    print("Waiting for client request..")


    s.listen(2)
    conn, addr = s.accept()
    connections.append(conn)
    eu.set_num_aggs(len(connections))
    print('Connected to :', addr[0], ':', addr[1])
    for connection in connections:
        start_new_thread(threaded, (connection, eu))
