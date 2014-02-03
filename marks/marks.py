#!/usr/bin/env python

import sys
import argparse
from configobj import ConfigObj
from random import randint

completedmission = {"MID": "MID1", "DAY": 1}

#SCALAR = [int(72 + i / 2) for i in range(1, 100)]
#SCALAR_CFP = [int(100 - i / 3) for i in range(1, 100)]
#SCALAR_NCFP = [int(80 + i / 2) for i in range(1, 100)]
#SCALAR_REP = [int(90 + i / 3) for i in range(1, 100)]
#SCALAR_PE = [100 for i in range(1, 100)]


SCALAR_CFP = [1.0] * 100
SCALAR_NCFP = [1.0] * 100
SCALAR_REP = [1.0] * 100
SCALAR_PE = [1.0] * 100


MAXNCFP = -30
NCFPPEN = -3
MAXCFP = 30
CFPBON = 3
CFPbon = 1
MAXREP = 20
MAXPE = 10
BASELINE = 50

# ASSOCIATED DAY, COMPLETED?, ON SCHEDULE?, no of REPS
MISSIONS = {"MID" + str(i): {"EXPECTEDDAY": i, "COMPLETED": False,
            "ONSCHEDULE": False, "REPS": 0} for i in range(1, 45)}
PERSONALELEMENTS = {"PE" + str(i): {"USED": False}
                    for i in range(1, 6)}


class Simulator:

    def __init__(self, configfile='marks.conf', outputfile='results.csv'):
        self.configfile = configfile

    def execute(self):
        m = Mark(userid=randint(1, 1000))
        history = []
        marksconfig = ConfigObj(self.configfile)

        for s in marksconfig.sections:

            print(('\n--->' + s))
            day = marksconfig[s]

            for operation in day.sections:

                params = list(day[operation].values())
                print(('Today we did', params))
                op = getattr(m, operation)
                for param in params:
                    op(param)

            m.endDay()
            m.newDay()
            m.getEvaluation()
            m.getNormEvaluation()
            history.append(str(m.normevaluation))
            print(('CURRENT STATUS', m))

        print(history)
        with open('results.csv', 'a') as f:
            f.write(",".join(history) + "\n")
            f.close()


class Mark:

    def __init__(self, userid):
        self.userid = userid
        self.currentday = 1
        self.acummulatedCFP = 0
        self.acummulatedNCFP = 0
        self.acummulatedREP = 0
        self.acummulatedPE = 0
        self.MISSIONS = MISSIONS
        self.PERSONALELEMENTS = PERSONALELEMENTS
        self.lastdayrep = 45
        self.oldevaluation = 0
        self.evaluation = 0
        self.normoldevaluation = 0
        self.normevaluation = 0

    def login(self):
        pass

    def __repr__(self):
        return """{0} - {1} - {2} \n
CFP {3}/ NCFP {4}/  REP{5}/ PE {6}/ NORM {7}""".format(self.userid,
        self.currentday, self.evaluation, self.acummulatedCFP,
        self.acummulatedNCFP, self.acummulatedREP,
        self.acummulatedPE, self.normevaluation)

    def endDay(self):
        self.checkMission()
        self.checkPE()

    def newDay(self):
        self.currentday += 1

    def doPE(self, personalelement):
        self.PERSONALELEMENTS[personalelement]["USED"] = True

    def checkPE(self):
        self.acummulatedPE = (MAXPE / 5) * sum([1 for PE in
        list(self.PERSONALELEMENTS.values()) if PE["USED"]])

    def doREP(self, repeatedmission):
        self.doMission(repeatedmission)

    def checkREP(self):
        self.checkMission()

    def doMission(self, mission):

        yumpmission = self.MISSIONS[mission]
        if not yumpmission["COMPLETED"]:
            yumpmission["COMPLETED"] = True

        if yumpmission["EXPECTEDDAY"] == self.currentday:
            yumpmission["ONSCHEDULE"] = True

        yumpmission["REPS"] = yumpmission["REPS"] + 1

        if yumpmission["REPS"] > 1:
            self.lastdayrep = self.currentday


    def checkMission(self):

        acummulatedCFP = sum([CFPBON for mission in list(self.MISSIONS.values())
                         if (mission["COMPLETED"] and mission["ONSCHEDULE"])]) +\
                         sum([CFPbon for mission in list(self.MISSIONS.values())
                         if (mission["COMPLETED"] and not mission["ONSCHEDULE"])])

        self.acummulatedCFP = min(MAXCFP, acummulatedCFP)

        acummulatedNCFP = sum([NCFPPEN for mission in list(self.MISSIONS.values())
                          if mission["EXPECTEDDAY"] <= self.currentday
                          and not mission["ONSCHEDULE"]])

        self.acummulatedNCFP = max(MAXNCFP, acummulatedNCFP)

        self.acummulatedREP = max(0, int(MAXREP / (1 + self.currentday -
                              self.getDayLastRep())))

    def getDayLastRep(self):
        return self.lastdayrep

    def getEvaluation(self):
        self.oldevaluation = self.evaluation
        evaluation = BASELINE + self.acummulatedCFP + self.acummulatedNCFP +\
                    self.acummulatedREP + self.acummulatedPE
        self.evaluation = evaluation


    def getNormEvaluation(self):

        self.oldnormevaluation = self.normevaluation
        print((self.currentday))
        normevaluation = BASELINE + self.acummulatedCFP*SCALAR_CFP[self.currentday] + \
                        self.acummulatedNCFP * SCALAR_NCFP[self.currentday] +\
                        self.acummulatedREP * SCALAR_REP[self.currentday] +\
                        self.acummulatedPE * SCALAR_PE[self.currentday]
        self.normevaluation = normevaluation


if __name__ == "__main__":

    s = Simulator
    parser = argparse.ArgumentParser(description='YUMP marks Simulator')

    parser.add_argument('--configfile', default='marks.conf',
                        help='Marks configuration file')
    parser.add_argument('--outputfile', default='results.csv',
                        help='Output file')

    args = vars(parser.parse_args())

    s = Simulator(args['configfile'], args['outputfile'])
    s.execute()

    sys.exit(0)

