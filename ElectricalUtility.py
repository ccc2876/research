import socket
from _thread import *
import threading
import pickle
import sys
from numpy import long



print_lock = threading.Lock()


class ElectricalUtility:
    """
    class for the electrical utility company
    includes a list of the values that the EU is sent at each time instance
    these values are comprised of the total of the secrets from the smart meteres
    """

    def __init__(self):
        self.values = []
        self.sums= []

    def add_reading(self, value):
        """
        adds a new value to the list
        :param value: the total consumption from all of the smart meters combined
        """
        self.values.append(value)

    def add_sums(self, x):
        self.sums.append(x)

    def return_values(self):
        """
        prints the list of values
        """
        return self.values


def threaded(conn, eu):
    data = conn.recv(1024)
    while True:
        if not data:
            print_lock.release()
            break
        else:
            val = pickle.loads(data)
            eu.add_sums(val)
            print(val)





def calculate_total(eu):
    total = long(abs(sum(eu.sums)))
    if not (total == 0):
        eu.add_reading(total)


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

    while True:

        s.listen(2)
        conn, addr = s.accept()
        connections.append(conn)
        print('Connected to :', addr[0], ':', addr[1])
        print_lock.acquire()
        start_new_thread(threaded, (conn, eu))
        print_lock.release()
        calculate_total(eu)
        print(eu.values)








