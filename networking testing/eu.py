import socket
import sys
import traceback
import threading
from ElectricalUtility import ElectricalUtility
from threading import Thread

print_lock = threading.Lock()

DELIMITER = "\n"

def main():
    start_server()


def start_server():
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
    sm_num = receive_input(connection, max_buffer_size)
    sm_num = int(sm_num[0])
    eu.set_num_sm(int(sm_num))
    is_active = True

    while is_active:
        input = receive_input(connection, max_buffer_size)
        print(input)
        if input:
            num_aggs = int(input[0])
            sm_id = int(input[1])
            value = int(input[2])
            eu.set_num_aggs(int(num_aggs))
            eu.add_sums(value, sm_id)
            print(eu.return_values())
        if not connection:
            break



def receive_input(connection, max_buffer_size):
    client_input = connection.recv(max_buffer_size)
    client_input_size = sys.getsizeof(client_input)
    if client_input_size > max_buffer_size:
        print("The input size is greater than expected {}".format(client_input_size))
    print(client_input.decode("utf8"))
    decoded_input = client_input.decode("utf8").split(DELIMITER)
    return decoded_input


def process_input(input_str):
    return str(input_str).upper()


if __name__ == "__main__":
    main()
