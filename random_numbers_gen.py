#!/usr/bin/env python
# coding: utf-8

# Purpose of code is to make list of random numbers for other things to use

from random import random
from random import sample


def random_int_c(amount):
    # Sample doesen't give same number twice so you can't have sample size over the range
    if amount>100:
        print("Can't produce that many original integers between 0-100")
        numbers=[]
        return
    try:
        numbers=sample(range(0, 100),amount)
    except ValueError:
        print('Sample size exceeded population size.')
        numbers=[]

    return numbers
    #sample(range(1, 100), amount)
    #print("")




def random_float():
    print(random())










def main():
    aa=100
    bb=random_int_c(aa)
    print(bb)
    #random_float()


if __name__ == '__main__':
    main()
