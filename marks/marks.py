#!/usr/bin/env python

import sys
import argparse
from configobj import ConfigObj
from random import randint

completedmission = {"MID":"MID1","DAY":1}

SCALAR = [int(72 + i/2) for i in range(1,47)]
SCALAR_CFP = [int(100 - i/3) for i in range(1,47)]
SCALAR_NCFP = [int(80 + i/2) for i in range(1,47)]
SCALAR_REP = [int(90 + i/3) for i in range(1,47)]
SCALAR_PE = [100 for i in range(1,47)]
	  

MAXNCFP = -30
NCFPPEN = -3
MAXCFP = 30
CFPBON = 3
CFPbon = 1
MAXREP = 20
MAXPE = 10
BASELINE = 50

# ASSOCIATED DAY, COMPLETED?, ON SCHEDULE?, no of REPS
MISSIONS = {"MID"+str(i):{"EXPECTEDDAY":i,"COMPLETED":False,"ONSCHEDULE":False,"REPS":0} for i in range(1,45)}
PERSONALELEMENTS = {"PE"+str(i):{"USED":False} for i in range(1,6)}


class Simulator:

    def __init__(self, configfile="marks.conf"):
        self.configfile = configfile

    def execute(self):

        m = MARK(userid=randint(1,1000))
        history = []
        marksconfig = ConfigObj(self.configfile)

        for s in marksconfig.sections:

            print("\n--->"+s)
            day = marksconfig[s]


            for operation in day.sections:

                params = list(day[operation].values())
                print("We did",params)
                op = getattr(m, operation)
                for param in params:
                    op(param)

                #op = getattr(m, operation.replace("do","check"))
                #op()


            m.endDay()
            m.newDay()
            m.getEvaluation()
            m.getNormEvaluation()
            history.append(str(m.normevaluation))
            print(m)

        print(history)
        f=open("results.csv","a")
        f.write(",".join(history)+"\n")
        f.close()

class MARK:

    
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
        
    def __str__(self):
        return """{0} - {1} - {2} \n
CFP {3}/ NCFP {4}/  REP{5}/ PE {6}/ NORM {7}""".format(self.userid,self.currentday,self.evaluation,self.acummulatedCFP,
                                            self.acummulatedNCFP,self.acummulatedREP,
                                                self.acummulatedPE,self.normevaluation)
        
    def endDay(self):
        self.checkMission()
        self.checkPE()
        
    def newDay(self):
        self.currentday += 1

    def doPE(self, personalelement):
                      
        self.PERSONALELEMENTS[personalelement]["USED"] = True

    def checkPE(self):
        self.acummulatedPE = (MAXPE/5) * sum([1 for PE in self.PERSONALELEMENTS.values() if PE["USED"]])

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


        acummulatedCFP = sum([CFPBON for mission in self.MISSIONS.values() if (mission["COMPLETED"] and mission["ONSCHEDULE"])]) +\
                 sum([CFPbon for mission in self.MISSIONS.values() if (mission["COMPLETED"] and not mission["ONSCHEDULE"])])

        self.acummulatedCFP =  min(MAXCFP,acummulatedCFP)

        acummulatedNCFP = sum([NCFPPEN for mission in self.MISSIONS.values() if mission["EXPECTEDDAY"] <= self.currentday and not mission["ONSCHEDULE"]])

        self.acummulatedNCFP =  max(MAXNCFP,acummulatedNCFP)


        self.acummulatedREP = max(0, int(MAXREP/(1+self.currentday-self.getDayLastRep())))





    def getDayLastRep(self):
                      
        return self.lastdayrep
            

    def getEvaluation(self):

        self.oldevaluation = self.evaluation
        evaluation = BASELINE + self.acummulatedCFP + self.acummulatedNCFP + self.acummulatedREP + self.acummulatedPE
        self.evaluation = evaluation


    def getNormEvaluation(self):

        self.oldnormevaluation = self.normevaluation
        normevaluation = BASELINE + self.acummulatedCFP*SCALAR_CFP[self.currentday]/100 + self.acummulatedNCFP*SCALAR_NCFP[self.currentday]/100 + self.acummulatedREP*SCALAR_REP[self.currentday]/100 + self.acummulatedPE*SCALAR_PE[self.currentday]/100
        self.normevaluation = normevaluation

        
if __name__=="__main__":

    s = Simulator
    parser = argparse.ArgumentParser(description='YUMP marks Simulator')

    parser.add_argument('--configfile', default='marks.conf', help='Marks configuration file')
    
    args = vars(parser.parse_args())

    s = Simulator(args['configfile'])
    s.execute()

    sys.exit(0)        
        
if __name__=="test":

    m = MARK(1)
    amission = {"MID":"MID1","DAY":1}
    m.addToCFP(amission)
    m.CFP()
    m.getEvaluation()
    m.endDay()
    m.newDay()
    amission = {"MID":"MID2","DAY":2}
    m.addToCFP(amission)
    m.CFP()
    amission = {"MID":"MID3","DAY":2}
    m.addToCFP(amission)
    m.CFP()
    m.getEvaluation()
    m.endDay()
    m.newDay()
    amission = {"MID":"MID2","DAY":3}
    m.addMISSIONREP(amission)
    m.REP()
    amission = {"MID":"MID3","DAY":3}
    m.addMISSIONREP(amission)
    m.REP()
    amission = {"MID":"MID2","DAY":3}
    m.addMISSIONREP(amission)
    m.REP()
    amission = {"MID":"MID3","DAY":3}
    m.addMISSIONREP(amission)
    m.REP()
    amission = {"MID":"MID2","DAY":3}
    m.addMISSIONREP(amission)
    m.REP()
    amission = {"MID":"MID3","DAY":3}
    m.addMISSIONREP(amission)
    m.REP()
    amission = {"MID":"MID2","DAY":3}
    m.addMISSIONREP(amission)
    m.REP()
    amission = {"MID":"MID3","DAY":3}
    m.addMISSIONREP(amission)
    m.REP()
    m.getEvaluation()
    for i in range(5):
        m.endDay()
        m.newDay()
        m.REP()
        m.getEvaluation()

    amission = {"MID":"MID4","DAY":7}
    m.addToCFP(amission)
    amission = {"MID":"MID5","DAY":7}
    m.addToCFP(amission)
    m.CFP()
    m.getEvaluation()
    m.endDay()
    m.newDay()

    amission = {"MID":"MID6","DAY":8}
    m.addToCFP(amission)
    amission = {"MID":"MID7","DAY":8}
    m.addToCFP(amission)
    m.CFP()
    m.getEvaluation()
    m.endDay()
    m.newDay()

    amission = {"MID":"MID8","DAY":11}
    m.addToCFP(amission)
    amission = {"MID":"MID9","DAY":11}
    m.addToCFP(amission)
    amission = {"MID":"MID10","DAY":11}
    m.addToCFP(amission)

    m.CFP()
    m.getEvaluation()
    m.endDay()
    m.newDay()

    amission = {"MID":"MID11","DAY":11}
    m.addToCFP(amission)
    m.CFP()
    m.getEvaluation()
    m.endDay()
    m.newDay()

    amission = {"MID":"MID12","DAY":12}
    m.addToCFP(amission)
    m.CFP()
    m.getEvaluation()

    m.addMISSIONREP(amission)
    m.REP()
    m.addMISSIONREP(amission)
    m.REP()
    m.getEvaluation()

    print(m.evaluation*SCALAR[m.currentday]/100.)
    m.endDay()











    
