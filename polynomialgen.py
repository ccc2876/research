import random
from sys import maxsize
"""
generates polynomials to be used to share secrets from a smart meter to the aggregator 
@author Claire Casalnova

add the number

"""


def create_poly(bin_string,secret,degree):
    power=degree
    polystring=""

    #loop over the binary string and generate the coefficients
    for i in range(0, len(bin_string)):
        if bin_string[i]==1:
            coeff=random.randint(0,maxsize)
            polystring+=str(coeff) + "x^" + str(power) + "+"

        power-=1

    #add the secret to the end of the polynomial as the constant
    polystring+=str(secret)
    print(polystring)

def get_info(degree,secret):
    #create a string of binary numbers for the x values
    bin_string=[1]

    #loop over the range of the degree to generate whether the power of x will be present
    for i in range(1,degree):
        bit=random.randint(0,1)
        bin_string.append(bit)



    create_poly(bin_string,secret,degree)

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
