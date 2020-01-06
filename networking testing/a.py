import socket
import sys
from Aggregator import Aggregator
import traceback
import time
from numpy import long
from threading import Thread


DELIMITER = "\n"


def start_server(connections, eu_conn):
    # set up connection to the smart meters
    TCP_IP = '127.0.0.1'
    TCP_PORT = int(sys.argv[1])
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((TCP_IP, TCP_PORT))

    num_smart_meters = 3
    num_smart_meters = str(num_smart_meters)
    num_smart_meters += DELIMITER
    eu_conn.sendall(num_smart_meters.encode("utf-8"))
    ID = int(sys.argv[2])
    print(sys.argv[1], " ", sys.argv[2])
    aggregator = Aggregator(ID, int(num_smart_meters))

    while len(connections) < int(num_smart_meters):
        s.listen()
        conn, addr = s.accept()
        print('Connected to :', addr[0], ':', addr[1])
        connections.append(conn)
        conn.sendall(str(aggregator.get_ID()).encode("utf-8"))
        try:
            Thread(target=clientThread, args=(conn, aggregator, TCP_IP, TCP_PORT, eu_conn)).start()
        except Exception as e:
            print(e)
            print("Thread did not start.")
            traceback.print_exc()





def clientThread(connection, aggregator, ip, port, eu_conn, max_buffer_size=5120):
    sm_id = receive_input(connection, max_buffer_size)
    time_length = int(receive_input(connection, max_buffer_size))
    agg_num = int(receive_input(connection, max_buffer_size))

    # agg_num = int(agg_num.strip(DELIMITER))
    aggregator.calculate_lagrange_multiplier(int(agg_num))
    counter = 0
    is_active = True
    shares = True
    while is_active:
        meter_id = int(sm_id)
        # print("sending id to eu of", sm_id)
        meter_id = str(meter_id) + DELIMITER
        meter_id = int(meter_id.strip(DELIMITER))
        is_active = False
        while shares:
            client_input = receive_input(connection, max_buffer_size)
            if client_input:
                print("Processed result: {}".format(client_input))
                aggregator.append_shares(int(client_input), meter_id)
                aggregator.update_totals(int(meter_id))
                constant = long(aggregator.get_current_total(meter_id)) * long(aggregator.get_lagrange_multiplier())
                aggregator.calc_sum(constant, meter_id)
                counter += 1
                if counter > time_length:
                    shares = False
            else:
                connection.close()
                print("Connection " + str(ip) + ":" + str(port) + " closed")
                sending_string = str(agg_num) + DELIMITER
                sending_string += str(meter_id) + DELIMITER
                val = aggregator.get_sum(meter_id)
                val = str(val) + DELIMITER
                sending_string += val
                # val = int(val.strip(DELIMITER))
                sending_string += "done\n"
                print(sending_string)
                eu_conn.sendall(sending_string.encode("utf-8"))
                shares = False


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


def main():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 8000
    try:
        soc.connect((host, port))
    except:
        print("Connection Error")
        sys.exit()

    connections = []
    start_server(connections, soc)
    for conn in connections:
        conn.close()



if __name__ == "__main__":
    main()
