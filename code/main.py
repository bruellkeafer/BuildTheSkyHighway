import random as rd
import numpy as np
import matplotlib.pyplot as plt

class Building:

    ReachableAntennas = []
    Score = 0

    def __init__(self,x,y,latencyWeight,connectionSpeedWeight):
        self.pos = [x,y]
        self.latencyWeight = latencyWeight
        self.connectionSpeedWeight = connectionSpeedWeight
    
    def findBestAntenna(self,antennas):
        bestAntenna = [0, None]
        for antenna in antennas:                
            score = getScore(self, antenna)
            if(score > bestAntenna[0]):
                bestAntenna = [score,antenna]
            if(distance(self, antenna) > antenna.range):
                score *= 0.000001
        if(bestAntenna[1] is None):
            bestAntenna = (0, antennas[rd.randint(0, len(antennas))])
        return bestAntenna

class Antenna:    
    def __init__(self, rangeValue, connectionSpeed):
      self.range = rangeValue
      self.connectionSpeedWeight = connectionSpeed
      self.pos = [None, None]
      self.assignedBuildings = []
    
    def assignBuilding(self,building):
      self.assignedBuildings.append(building)

    def listReachableBuildings(self,buildingsList):
        for a in buildingsList:
            if(distance(self.X,self.Y,a.X,a.Y) <= a.Range):
                self.ReachableAntennas.append(a)

class Clustering:
    def __init__(self, antennas, buildings):
      self.antennas = antennas
      self.buildings = buildings
      self.NumberOfAntennas = len(antennas)
      for antenna in self.antennas:
        antenna.pos = [rd.randint(0,MapXLength), rd.randint(0,MapYLength)]
      
    def clusterStep(self):
      #build cluster groups
      for index , building in enumerate(self.buildings):
        print("processing building " + str(index) + '/' + str(len(self.buildings)))
        resultTuple = building.findBestAntenna(self.antennas)
        _ , antenna = resultTuple
        antenna.assignBuilding(building)

      for antenna in self.antennas:
        if len(antenna.assignedBuildings) != 0:
            antenna.pos = np.round(np.average(list(map(lambda building : building.pos[0], antenna.assignedBuildings)))),np.round(np.average(list(map(lambda building : building.pos[1], antenna.assignedBuildings))))
        #antenna.pos = np.round(np.average(list(map(lambda building : building.pos, antenna.assignedBuildings)),axis = 1))

def distance(building,antenna):
    return np.linalg.norm(np.array(building.pos) - np.array(antenna.pos))

def totalScore(buildings, reward):
    if(any(hasattr(x, 'Score') for x in buildings)):
        return 0
    return sum(list(map(lambda x : x.Score, buildings))) + reward

def getScore(building,antenna):

  return (building.connectionSpeedWeight * antenna.connectionSpeedWeight) - (building.latencyWeight * distance(antenna,building))

def connectBuildingToAntenna(building):
    building.connectedAntenna = max(list(map(lambda x : getScore(building,x), building.ReachableAntennas)))

file=open("C:\\Users\\Tim Martins\\Desktop\\Projekte\\Programmieren\\ReplyChallenges\\TapTapTap\\BuildTheSkyHighway\\data_scenarios_b_mumbai.in","r")

string = file.read()
inputs = string.split("\n")
#Line 1 - Map Read
MapScale = inputs[0].split(" ")
MapXLength = int(MapScale[0])
MapYLength = int(MapScale[1])
#Line 2 - Resources Read
ResourceInformation = inputs[1].split(" ")
BuildingsCount = int(ResourceInformation[0])
AntennasCount = int(ResourceInformation[1])
RewardValue = int(ResourceInformation[2])
#Buildings Read
Buildings = []
for i in range(BuildingsCount):
    buildingInformation = inputs[i+2].split(" ")
    Buildings.append(Building(
        int(buildingInformation[0]),
        int(buildingInformation[1]),
        int(buildingInformation[2]),
        int(buildingInformation[3]),
    ))
#Antennas Read
Antennas = []
for i in range(AntennasCount):
    antennaInformation = inputs[i+BuildingsCount+2].split(" ")
    Antennas.append(Antenna(
        int(antennaInformation[0]),
        int(antennaInformation[1])
    ))

def plot_map(antennas,buildings):
    plt.scatter(np.array(list(map(lambda building : building.pos, buildings)))[:,0], np.array(list(map(lambda building : building.pos, buildings)))[:,1])
    plt.scatter(np.array(list(map(lambda antenna : antenna.pos, antennas)))[:,0], np.array(list(map(lambda antenna : antenna.pos, antennas)))[:,1])
    plt.show()

print("create cluster")
cl = Clustering(Antennas,Buildings)
print("created cluster")
#plot_map(Antennas,Buildings)

print("processing cluster step")
cl.clusterStep()
print("cluster step finished")

for c in cl.antennas:
    print(c.pos)
#plot_map(Antennas,Buildings)
outFile = open("C:\\Users\\Tim Martins\\Desktop\\Projekte\\Programmieren\\ReplyChallenges\\TapTapTap\\BuildTheSkyHighway\\out.txt","w")
outString = str(len(cl.antennas)) + "\n"
for index,antenna in enumerate(cl.antennas):
    outString += str(index) + " " + str(int(antenna.pos[0])) + " " + str(int(antenna.pos[1])) + "\n"


outFile.write(outString)

