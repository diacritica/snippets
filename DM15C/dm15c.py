#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This script only makes sense to people owning a DM-15C from
# http://www.rpn-calc.ch/ a HP 15C clone that enables very basic
# serial communication through a miniUSB port

import serial
import sys


def segtofloat(entryLines):
    #print "entryLines->", entryLines
    topline = entryLines[0][5:55]
    middleline = entryLines[1][5:55]
    bottomline = entryLines[2][5:55]

    mantisasign = entryLines[1][2:4]
    expsign = entryLines[1][41:43]

    arraynum = ["", "", "", "", "", "", "", "", "", ""]
    toplinepos = [1, 6, 11, 16, 21, 26, 31, 36, 41, 46]

    for i in toplinepos:
        tempdigit = topline[i:i + 2]
        if tempdigit == "__": arraynum[toplinepos.index(i)] += "a"

    middlelinepos = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45]
    for i in middlelinepos:
        tempdigit = middleline[i:i + 4]

        # Check if there is a blinking screen (error)
        try:
            if tempdigit[0] == "|": arraynum[middlelinepos.index(i)] += "f"
        except:
            print "Error in DM15C"
            sys.exit()

        if tempdigit[1:3] == "__": arraynum[middlelinepos.index(i)] += "g"
        if tempdigit[-1] == "|": arraynum[middlelinepos.index(i)] += "b"

    bottomlinepos = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45]
    for i in bottomlinepos:
        tempdigit = bottomline[i:i + 4]
        if tempdigit[0] == "|": arraynum[bottomlinepos.index(i)] += "e"
        if tempdigit[1:3] == "__": arraynum[bottomlinepos.index(i)] += "d"
        if tempdigit[-1] == "|": arraynum[bottomlinepos.index(i)] += "c"

    truthmatrix = ["afbedc", "bc", "agbed", "agbdc", "fgbc",\
    "afgdc", "afgedc", "abc", "afgbedc", "afgbdc"]

    result = [str(truthmatrix.index(i)) for i in arraynum if i in truthmatrix]

    #print "result->", result

    mantisapart = "+"
    expsignpart = "+"

    if len(result) != 8:  # We know 8 is the only legit length for our array
        number = "424242e37"  # a fake number that represents a useless result
    else:
        integerpart = result[0]
        fractionpart = "".join(result[1:6])
        exppart = "".join(result[6:8])

        if mantisasign == "__": mantisapart = "-"
        if expsign == "__": expsignpart = "-"

        number = mantisapart + integerpart + "." + fractionpart +\
         "e" + expsignpart + exppart

    floatnumber = float(number)
    # This is where you should react to specific numbers
    # For now, I'll just print it'
    print "->", floatnumber


if __name__ == "__main__":

    ser = serial.Serial('/dev/ttyUSB0', 38400)  # YOU SHOULD CHANGE THIS
    linesList = []
    count = 1

    while True:
        line = ser.readline()
        if line != "Disp off\r\n":  # We must ignore this message
            linesList.append(line)

            if count % 5 == 0:
                segtofloat(linesList)
                linesList = []

            count += 1
