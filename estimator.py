import util,random,collections,math
from util import Belief, pdf
from engine.const import Const

# Class: Estimator
#----------------------
# Maintain and update a belief distribution over the probability of a car being in a tile.
class Estimator(object):

    def __init__(self, numRows: int, numCols: int):
        self.belief = util.Belief(numRows, numCols)
        self.transProb = util.loadTransProb()
        self.transProbDict = dict()
        for (t1, t2) in self.transProb:
            if not t1 in self.transProbDict:
                self.transProbDict[t1] = collections.Counter()
            self.transProbDict[t1][t2] = self.transProb[(t1,t2)]

        self.particles = collections.Counter()
        potentialParticles = list(self.transProbDict.keys())
        for i in range(200):
            particleIndex = int(random.random() * len(potentialParticles))
            self.particles[potentialParticles[particleIndex]] += 1

        newBelief = util.Belief(self.belief.getNumRows(), self.belief.getNumCols(), 0)
        for tile in self.particles:
            newBelief.setProb(tile[0], tile[1], self.particles[tile])
        newBelief.normalize()
        self.belief = newBelief

    def GiveRandom(self,w_dict):
        weights = []
        for i in w_dict:
            weights.append([ i , w_dict[i] ])
        t = 0
        for i in weights:
            t = t + i[1]
        random_value = random.uniform(0,t)
        j = 0
        while(j < len(weights)):
            random_value =  random_value - weights[j][1]
            if random_value < 0:
                return weights[j][0]
            j = j + 1
    def estimate(self, posX: float, posY: float, observedDist: float, isParked: bool) -> None:
        weights = {}
        for tile, occurrences in self.particles.items():
            weights[tile] = 0
            r, c = tile
            dist = math.sqrt((util.rowToY(r) - posY)**2 + (util.colToX(c) - posX)**2)
            pdf = util.pdf(observedDist, Const.SONAR_STD, dist)
            weights[tile] = pdf * occurrences
        newParticles = collections.Counter()
        for p in range(200):
            tile = self.GiveRandom(weights)
            newParticles[tile] += 1
        self.particles = newParticles
        newBelief = util.Belief(self.belief.getNumRows(), self.belief.getNumCols(), 0)
        for tile in self.particles:
            newBelief.setProb(tile[0], tile[1], self.particles[tile])
        newBelief.normalize()
        self.belief = newBelief
        return
    def getBelief(self) -> Belief:
        return self.belief
