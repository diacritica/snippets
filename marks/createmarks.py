#!/usr/bin/env python

import sys
import argparse
from configobj import ConfigObj
from random import randint,choice

mode = "PASSIVE"

if mode == "ACTIVE":
    n1 = 4
    n2 = 4
    n3 = 4
    n4 = 10

elif mode == "PASSIVE":
    n1 = 2
    n2 = 1
    n3 = 1
    n4 = 5


if __name__=="__main__":

    config = ConfigObj()
    config.filename = "mytest.conf"

    subsections = ["doMission","doREP","doPE"]

    for i in range(1,45):
        myday = "DAY "+str(i)
        config[myday] = {}
        for n in range(randint(1,n1)):
            subsection = choice(subsections)

            if subsection == "doMission":
                nomissions = randint(1,n2)
                missions = []
                for m in range(nomissions):
                    options = range(1,i+1)+[i]*i
                    print("OPTIONS->",options)
                    mn = choice(options)
                    mstr = "MID"+str(mn)
                    missions.append(mstr)
                adict = {"doMission":{ "mission"+m:m for m in missions  }}
                config["DAY "+str(i)].update(adict)
            elif subsection == "doREP":
                nomissions = randint(1,n3)
                missions = []
                for m in range(nomissions):
                    mn = choice(range(1,i+1))
                    mstr = "MID"+str(mn)
                    missions.append(mstr)
                adict = {"doREP":{ "rep"+m:m for m in missions  }}
                config["DAY "+str(i)].update(adict)

            elif subsection == "doPE":
                p = randint(1,100)
                if p<n4:
                    adict = {"doPE":{ "PE": "PE"+str(randint(1,5)) }}
                    config["DAY "+str(i)].update(adict)


    print(config)            
    config.write()            
