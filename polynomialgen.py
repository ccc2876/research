import random
from sys import maxsize


"""x4 x3 x2 x1 secet """

def create_poly(vars,secret):
    print(vars)
    poly=""
    for i in range(0,len(vars)-1):
        if vars.pop(i)==1:
            coeff=random.randint(1,maxsize)
            poly+=str(coeff)+"x" + "+"


    poly+=str(secret)
    print(poly)

def get_info(agg,sm,secret):
    deg_max=agg-1
    degree=random.randint(1,deg_max)

    bin_string=[]

    for i in range(0,degree):
        bit=random.randint(0,1)
        bin_string.append(bit)


    create_poly(bin_string,secret)

def get_inputs():
    aggregators = int(input("How many aggregators?"))
    while aggregators<1:
        aggregators = int(input("How many aggregators?"))

    sm=int(input("How many smart meters?"))
    while sm < 1:
        sm = int(input("How many smart meters?"))

    secret=int(input("What is the secret?"))
    while secret < 1:
        secret=int(input("What is the secret?"))

    get_info(aggregators,sm,secret)

def main():
    get_inputs()



main()