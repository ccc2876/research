import socket
import sys
import traceback
from ElectricalUtility import ElectricalUtility
from threading import Thread


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
    # infinite loop- do not reset for every requests
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
    print("new thread")
    sm_num = int(receive_input(connection, max_buffer_size))
    num_aggs = receive_input(connection, max_buffer_size)
    eu.set_num_sm(int(sm_num))
    eu.set_num_aggs(int(num_aggs))
    is_active = True

    while is_active:
        sm_id = int(receive_input(connection, max_buffer_size))

        is_active = False
        id= True
        while id:
            client_input = receive_input(connection, max_buffer_size)
            if client_input:
                if client_input == "DONE":
                    break
                print("input:", int(client_input))
                eu.add_sums(int(client_input), int(sm_id))
                print(eu.return_values())
                is_active = True

            else:
                is_active = True
                id= False



def receive_input(connection, max_buffer_size):
    client_input = connection.recv(max_buffer_size)
    client_input_size = sys.getsizeof(client_input)
    if client_input_size > max_buffer_size:
        print("The input size is greater than expected {}".format(client_input_size))
    decoded_input = client_input.decode("utf8").rstrip()
    result = process_input(decoded_input)
    return result


def process_input(input_str):
    return str(input_str).upper()


if __name__ == "__main__":
    main()
