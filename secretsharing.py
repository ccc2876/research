import time
import copy
import random
from ElectricalUtility import ElectricalUtility
from Aggregator import Aggregator
from SmartMeter import SmartMeter
from numpy import long


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

    out = open("outputfiles/" + "T" + str(time_instances) + "A" + str(aggregators) + "S" + str(sm_num) + ".txt", "w")

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

    counter = 0

    for i in range(0, len(aggregator_list)):
        a = aggregator_list[counter]
        top = ""
        bottom = 1

        for a2 in aggregator_list:
            if not a2.get_ID() == a.get_ID():
                top += "(x - " + str(a2.get_ID()) + ")"
                bottom *= (a.get_ID() - a2.get_ID())
                a.set_lagrange(top + "/" + str(bottom))

        counter += 1
        print(a.lagrange)

    # begin loop on the number of time instances given
    for t in range(0, time_instances):
        out.write("Time instance " + str(t) + "\n\n")

        # generate a random number as the secret for the smart meter
        secret_total = 0
        for i in range(0, sm_num):
            secret = random.randint(1, 5)
            secret_total += secret

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
                single_share_time_start = time.time()
                sm.create_shares(aggregator)
                single_share_time_end = time.time()
                sm.add_time(single_share_time_end- single_share_time_start)

            sm.get_time()

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
            constant = long(a.get_current_total()) * long(a.get_lagrange_multiplier())
            constants.append(long(constant))

        # send the data to the electric utility company
        eu.add_reading(long(abs(sum(constants))))
        for e in eu.return_values():
            out.write("%d" % e)
            out.write("\n")
        out.write("\n")
        print(end-start)
        print(secret_total)
        # close the file
    out.close()
    f.close()


main()
