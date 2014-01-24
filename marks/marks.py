#!/usr/bin/env python


completedmission = {"MID":"MID1","DAY":1}

SCALAR = [int(72 + i/2) for i in range(1,45)]
SCALAR_CFP = [int(100 - i/3) for i in range(1,45)]
SCALAR_NCFP = [int(80 + i/2) for i in range(1,45)]
SCALAR_REP = [int(90 + i/3) for i in range(1,45)]
SCALAR_AEP = [100 for i in range(1,45)]
	  

MAXNCFP = -30
MAXCFP = 30
MAXREP = 20
MAXPE = 10
BASELINE = 50

# ASSOCIATED DAY, COMPLETED?, ON SCHEDULE?, no of REPS
MISSIONS = {"MID"+str(i):{"EXPECTEDDAY":i,"COMPLETED":False,"ONSCHEDULE":False,"REPS":0} for i in range(1,45)}
PERSONALELEMENTS = {"PE"+str(i):{"REPEATED":False} for i in range(5)}


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
        self.lastdayrep = -1
        self.oldevaluation = 0
        self.evaluation = 0

    def login(self):
        pass
        
    def __str__(self):
        return """{0} - {1} - {2} \n
{3}/{4}/{5}/{6}\n
{7}""".format(self.userid,self.currentday,self.evaluation,self.acummulatedCFP,
                                            self.acummulatedNCFP,self.acummulatedREP,
                                                self.acummulatedPE,"")
        
    def endDay(self):
        print("END DAY",self)
        self.checkNCFP()
        
    def newDay(self):
        print("NEW DAY")
        self.currentday += 1

    def doMission(self, completedmission):

        yumpmission = self.MISSIONS[completedmission["MID"]]
        
        if yumpmission["EXPECTEDDAY"] == self.currentday:
            yumpmission["ONSCHEDULE"] == True

        if not yumpmission["COMPLETED"]:
            yumpmission["COMPLETED"] == True
            self.CFP()


        yumpmission["REPS"] == yumpmission["REPS"] + 1
        if yumpmission["REPS"] > 1:
            self.REP()
            

    def checkNCFP(self):

        acummulatedNCFP = sum([-1 for mission in self.MISSIONS.values() if mission[0] <= 1 and not mission[1]])
        self.acummulatedNCFP =  max(MAXNCFP,acummulatedNCFP)
        
    
        
    def addToCFP(self, completedmission):

        if self.MISSIONS[completedmission["MID"]][0] == self.currentday:
            self.MISSIONS[completedmission["MID"]][2] = True            


        self.MISSIONS[completedmission["MID"]][1] = True
        
    def CFP(self):
        
        acummulatedCFP = sum([3 for mission in MISSIONS.values() if (mission[1] and mission[2])]) +\
                 sum([1 for mission in self.MISSIONS.values() if (mission[1] and not mission[2])])

        self.acummulatedCFP =  min(MAXCFP,acummulatedCFP)

    def addMISSIONREP(self, repeatedmission):

        self.MISSIONS[repeatedmission["MID"]][3] += 1
        self.lastdayrep = self.currentday

    def REP(self):

        self.acummulatedREP = max(0, int(MAXREP * (1-(self.currentday-self.getDayLastRep())/self.currentday)))

    def getDayLastRep(self):
                      
        return self.lastdayrep
            
    def addPE(self, personalelement):
                      
        self.PERSONALELEMENTS[personalelement["PE"]][0] = True

    def delPE(self, personalelement):

        self.PERSONALELEMENTS[personalelement["PE"]][0] = False

    def PE(self):
        self.acummulatedPE = MAXPE * (1-(5-sum([1 for PE in self.PERSONALELEMENTS.values() if PE[0]])))


    def getEvaluation(self):

        self.oldevaluation = self.evaluation
        evaluation = BASELINE + self.acummulatedCFP + self.acummulatedNCFP + self.acummulatedREP + self.acummulatedPE
        self.evaluation = evaluation

        
        
        
        
if __name__=="__main__":

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











    