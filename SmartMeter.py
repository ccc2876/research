import random
import socket
import sys
import traceback
import time
from numpy import long
from queue import Queue
from threading import Thread, Lock
from memory_profiler import profile


#global variables
g = -1 
n = -1
total_count = 0 # total count of readings
num_sm = 5 #number of smart meters in the network
total_readings = 1 #total reading values
time_instances = 1 #number of time instances
server_done = False

lock = Lock()


def get_readings():
	"""
	gets the random number value reading as the consumption
	"""
    read = random.randint(1, 10)
    print("Read", int(read))
    return read


@profile #this is how the program determines the memory usage
def encrypt(read):
	"""
	homomorphic encryption algorithm
	"""
    global g, n
    start =time.perf_counter()
    r = random.randint(1, g)
    encrypted_val = ((g ** read) * (r ** n)) % (n ** 2)
    end = time.perf_counter()
    print(end-start)
    print("e", encrypted_val)
    return encrypted_val


def receive_input(connection, max_buffer_size=5120):
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
    decoded_input = client_input.decode("utf8").rstrip()
    print("Dec", decoded_input)
    return decoded_input


def setup_client(host, port):
	"""
	sets up each smart meter as a client
	"""
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("host", host)
    print("port", port)
    print(soc)

    try:
        soc.connect((host, int(port)))
        port += 1
    except:
        print("Connection Error")
        sys.exit()
    return soc


def server_client_func(soc):
	"""
	sets up the special smart meter as the server to the other smart meters and a client to the electrical utility company
	"""
    global n, g
    inp = receive_input(soc)
    values = inp.split(" ")
    n = int(values[0])
    g = int(values[1])
    print("pub", n, g)
    public_key = str(n) + " " + str(g)
    return public_key


def only_client_func(soc):
	"""
	for smart meters that do not interact with utility company
	gets the publi key from the server
	for each time instance the smart meter gets a reading encrypts and sends to the special smart meter
	"""
    global n, g

    inp = receive_input(soc)
    values = inp.split(" ")
    n = int(values[0])
    g = int(values[1])
    print("n", n)
    print("g", g)

    for i in range(0, time_instances):
        read = get_readings()
        encrypted_val = encrypt(read)
        soc.sendall(str(encrypted_val).encode("utf-8"))
		time.sleep(0.5)


def wait_on_values(soc, public_key, queue):
	"""
	the server smart meter waits to receive all the readings from all
	the other smart meters before sending to the utility compnay
	"""
    global total_count, num_sm, total_readings, server_done
    soc.sendall(str(public_key).encode("utf-8"))

    if not server_done:
        for i in range(0, time_instances):
            read = get_readings()
            lock.acquire()
            total_readings *= int(encrypt(read))
            server_done = True
            total_count += 1
            lock.release()
    for i in range(0, time_instances):
        lock.acquire()
        total_readings *= int(receive_input(soc))
        print("tr:", total_readings)
        print("tc", total_count)
        lock.release()
        time.sleep(1)


def send_final(soc, final):
	"""
	smart meter server sends final value to utility company
	"""
    print(final)
    lock.acquire()
    soc.sendall(str(final).encode("utf-8"))
    lock.release()


def setup_special_sm(host, port, is_server=1):
	"""
	calls functions to set up the server smart meter
	"""
    conn = setup_client(host, port)
    public_key = server_client_func(conn)
    start_server(public_key, conn)


def start_server(public_key, conn):
	"""
	starts the smart meter server on the host ip
	"""
    global num_sm
    # sets up server for connections to other smart meters
    sm_connections = []
    host = "129.21.67.150"  # will be VM ip
    port = 8001  # make the id of smart meter + 8000
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Socket created")
    try:
        soc.bind((host, port))
    except:
        print("Bind failed. Error : " + str(sys.exc_info()))
        sys.exit()
    soc.listen(num_sm)  # queue up to num sm request
    print("Socket now listening on port ", port)
    queue = Queue()

    print("len", len(sm_connections))
    print(num_sm - 1)
    while len(sm_connections) <= (num_sm - 2): 
        connection, address = soc.accept()
        sm_connections.append(connection)
        ip, port = str(address[0]), int(address[1])
        print("Connected with " + ip + ":" + str(port))
        port += 1
        try:
            t = Thread(target=wait_on_values, args=(connection, public_key, queue))
            t.start()
            t.join()
        except:
            print("Thread did not start.")
            traceback.print_exc()

    send_final(conn, int((total_readings % (n ** 2))))


def main():
	"""
	runs the program
	"""
    global n, g

    host = sys.argv[1]
    port = int(sys.argv[2])
    is_server = int(sys.argv[3])  # boolean flag for special smart meter
    print(is_server)
    if is_server:
        setup_special_sm(host, port)
    else:
        conn = setup_client(host, port)
        only_client_func(conn)
        time.sleep(1)


if __name__ == '__main__':
    main()