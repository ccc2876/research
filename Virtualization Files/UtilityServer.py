__author__ = "Claire Casalnova"

import socket
import sys
import traceback
from ElectricalUtility import ElectricalUtility
from threading import Thread,Lock


DELIMITER = "\n"
print_lock = Lock()
print_cycle = 1

def main():
    start_server()


def start_server():
    """
    set up the connection to each of the aggregators
    start a thread for each connection
    """
    eu = ElectricalUtility()
    connections = []
    host = "127.0.0.1"
    port = 8000  # arbitrary non-privileged port
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Socket created")
    try:
        soc.bind((host, port))
    except:
        print("Bind failed. Error : " + str(sys.exc_info()))
        sys.exit()
    soc.listen(6)  # queue up to 6 requests
    print("Socket now listening")

    while True:
        connection, address = soc.accept()
        connections.append(connection)
        eu.set_num_aggs(len(connections))
        ip, port = str(address[0]), str(address[1])
        print("Connected with " + ip + ":" + port)
        try:
            Thread(target=clientThread, args=(connection,eu, ip, port)).start()
        except:
            print("Thread did not start.")
            traceback.print_exc()


def clientThread(connection, eu, ip, port, max_buffer_size=5120):
    """
    thread for each connection to an aggregator
    :param connection: the specific connection
    :param eu: the utility company object
    :param ip: the ip address of the connection
    :param port: the port of the connection
    :param max_buffer_size: the max buffer size set to 5120
    """

    global print_cycle
    sm_num = receive_input(connection, max_buffer_size)
    sm_num = int(sm_num[0])
    print_lock.acquire()
    eu.set_num_sm(int(sm_num))
    print_lock.release()
    is_active = True
    counter = 1
    while is_active:
        # receive the input from the aggregators and process it in the utility company object
        client_input = receive_input(connection, max_buffer_size)
        counter += 1

        # print("receiving...", client_input)
        if client_input:
            num_aggs = int(client_input[0])
            sm_id = int(client_input[1])
            bill_boolean = int(client_input[2])

            # if counter == eu.get_num_aggs():
            #     print("bill amount:", int(client_input[3]))
            #     print_lock.acquire()
            #     eu.generate_bill(sm_id, int(client_input[3]))
            #     print_lock.release()
            #     is_active = False
            # else:
            value = int(client_input[3])
            print_lock.acquire()
            eu.set_num_aggs(int(num_aggs))
            eu.set_spatial_sum(value)
            if print_cycle % num_aggs == 0:
                print(eu.get_spatial_sum())
                print_cycle = 1
            else:
                print_cycle += 1
            print_lock.release()


def receive_input(connection, max_buffer_size):
    """
    function for receiving and decoding input from the smart meters
    :param connection: the connection the smart meter
    :param max_buffer_size: the max buffer size of receiving input
    :return: the decoded input
    """
    client_input = connection.recv(max_buffer_size)
    client_input_size = sys.getsizeof(client_input)
    if client_input_size > max_buffer_size:
        print("The input size is greater than expected {}".format(client_input_size))
    decoded_input = client_input.decode("utf8").split(DELIMITER)
    return decoded_input


if __name__ == "__main__":
    main()
