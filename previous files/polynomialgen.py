import random
from sys import maxsize
"""
generates polynomials to be used to share secrets from a smart meter to the aggregator 
@author Claire Casalnova

add the number

"""






def get_inputs():

    #ask for number of aggregators
    aggregators = int(input("How many aggregators? "))
    while aggregators<1:
        aggregators = int(input("How many aggregators? "))

    #calculate degree
    degree = aggregators - 1
   # degree = random.randint(int(deg_max/2), deg_max)


    #ask for number of smart meters
    sm=int(input("How many smart meters? "))
    while sm < 1:
        sm = int(input("How many smart meters? "))

    #ask for the secret for each of the smart meters
    for i in range(1, sm+1):
        secret=int(input("What is the secret for Smart Meter #" + str(i) + "? "))
        while secret < 1:
            secret=int(input("What is the secret for Smart Meter #" + str(i) + "? "))

        get_info(degree,secret)

def main():
    get_inputs()



main()
