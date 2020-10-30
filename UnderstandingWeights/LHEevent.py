import ROOT as rt

                     
class LHEevent():
    
    def __init__(self):
        self.Particles = []
        self.Weights = []
        self.Model = "NONE"
        
    def fillEvent(self, lheLines):
        for i in range(2,len(lheLines)-1):
            self.Particles.append(self.readParticle(lheLines[i]))
        return 1

    def fillWeight(self, lheLines):
        for i in range(1,len(lheLines)-1):
            self.Weights.append(self.readWeight(lheLines[i]))
        return 1

    def readWeight(self, lheLine):
        #dataIN = lheLine[:-1].split(" ")
        dataIN = lheLine.split()
        #print dataIN
        dataINgood = []
        for entry in dataIN:
            if entry != "": dataINgood.append(entry)
        id = str(dataINgood[1])
        id = id.replace(">", "")
        id = id.replace("'", "")
        id = id.replace("id=", "")
        #print dataINgood[2]
        return {'weightID': id,
                'weightValue': float(dataINgood[2])} 

    def readParticle(self, lheLine):
        dataIN = lheLine[:-1].split(" ")
        dataINgood = []
        for entry in dataIN:
            if entry != "": dataINgood.append(entry)
        return {'ID': int(dataINgood[0]),
                'mIdx': int(dataINgood[2])-1,
                'Px' : float(dataINgood[6]),
                'Py' : float(dataINgood[7]),
                'Pz' : float(dataINgood[8]),
                'E' : float(dataINgood[9]),
                'M' : float(dataINgood[10])}
