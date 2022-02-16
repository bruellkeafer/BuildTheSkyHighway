import random as rd
import numpy as np
import matplotlib.pyplot as plt
import time

startTime = time.time()
import multiprocessing as mp


class Building:
    #ReachableAntennas = []
    Score = 0

    def __init__(self, x, y, latency_weight, connection_speed_weight):
        self.pos = [x, y]
        self.latencyWeight = latency_weight
        self.connectionSpeedWeight = connection_speed_weight

    def find_best_antenna(self, antennas):
        best_antenna = [0, None]
        for ant in antennas:
            score = get_score(self, ant)
            if score > best_antenna[0]:
                best_antenna = [score, ant]
            if distance(self, ant) > ant.range:
                score *= 0.000001
        if best_antenna[1] is None:
            best_antenna = (0, antennas[rd.randint(0, len(antennas) - 1)])
        return best_antenna


class Antenna:
    def __init__(self, range_value, connection_speed):
        self.range = range_value
        self.connectionSpeedWeight = connection_speed
        self.pos = [None, None]
        self.assignedBuildings = []

    def assign_building(self, building):
        self.assignedBuildings.append(building)


class Clustering:
    def __init__(self, antennas, buildings):
        self.antennas = antennas
        self.buildings = buildings
        self.NumberOfAntennas = len(antennas)
        for ant in self.antennas:
            new_pos = [rd.randint(0, MapXLength - 1), rd.randint(0, MapYLength - 1)]
            while position_already_used(new_pos, antennas):
                new_pos = [rd.randint(0, MapXLength - 1), rd.randint(0, MapYLength - 1)]
            ant.pos = new_pos

    def cluster_step(self):
        # build cluster groups
        for index, building in enumerate(self.buildings):
            self.assign_building_to_best_antennas(building, index)
        self.shift_antenna_positions()

    def assign_building_to_best_antennas(self, building, index):
        print("processing building " + str(index) + '/' + str(len(self.buildings)))
        _, ant = building.find_best_antenna(self.antennas)
        ant.assign_building(building)

    def shift_antenna_positions(self):
        for a in self.antennas:
            if len(a.assignedBuildings) != 0:
                a.pos = np.round(
                    np.average(list(map(lambda bld: bld.pos[0], a.assignedBuildings)))), np.round(
                    np.average(list(map(lambda bld: bld.pos[1], a.assignedBuildings))))


def position_already_used(pos, antennas):
    print("position already used")
    for ant in antennas:
        if ant.pos[0] == pos[0] and ant.pos[1] == pos[1]:
            return True
    return False


def distance(building, ant):
    return np.linalg.norm(np.array(building.pos) - np.array(ant.pos))


def total_score(buildings, reward):
    if any(hasattr(x, 'Score') for x in buildings):
        return 0
    return sum(list(map(lambda x: x.Score, buildings))) + reward


def get_score(building, ant):
    return (building.connectionSpeedWeight * ant.connectionSpeedWeight) - (
            building.latencyWeight * distance(ant, building))


#def connect_building_to_antenna(building):
  #  building.connectedAntenna = max(list(map(lambda x: get_score(building, x), building.ReachableAntennas)))



file = open(
    "C:\\Users\\Tim Martins\\Desktop\\Projekte\\Programmieren\\ReplyChallenges\\TapTapTap\\BuildTheSkyHighway"
    "\\data_scenarios_b_mumbai.in",
    "r")

string = file.read()
inputs = string.split("\n")
# Line 1 - Map Read
MapScale = inputs[0].split(" ")
MapXLength = int(MapScale[0])
MapYLength = int(MapScale[1])
# Line 2 - Resources Read
ResourceInformation = inputs[1].split(" ")
BuildingsCount = int(ResourceInformation[0])
AntennasCount = int(ResourceInformation[1])
RewardValue = int(ResourceInformation[2])
# Buildings Read
Buildings = []
for i in range(BuildingsCount):
    buildingInformation = inputs[i + 2].split(" ")
    Buildings.append(Building(
        int(buildingInformation[0]),
        int(buildingInformation[1]),
        int(buildingInformation[2]),
        int(buildingInformation[3]),
    ))
# Antennas Read
Antennas = []
for i in range(AntennasCount):
    antennaInformation = inputs[i + BuildingsCount + 2].split(" ")
    Antennas.append(Antenna(
        int(antennaInformation[0]),
        int(antennaInformation[1])
    ))


def plot_map(antennas, buildings):
    plt.scatter(np.array(list(map(lambda bld: bld.pos, buildings)))[:, 0],
                np.array(list(map(lambda bld: bld.pos, buildings)))[:, 1])
    plt.scatter(np.array(list(map(lambda ant: ant.pos, antennas)))[:, 0],
                np.array(list(map(lambda ant: ant.pos, antennas)))[:, 1])
    plt.show()


print("create cluster")
cl = Clustering(Antennas, Buildings)
print("created cluster")

print("processing cluster step")
cl.cluster_step()
print("cluster step finished")

for c in cl.antennas:
    print(c.pos)

outFile = open(
    "..\\out.txt",
    "w")
outString = str(len(cl.antennas)) + "\n"
for index, antenna in enumerate(cl.antennas):
    outString += str(index) + " " + str(int(antenna.pos[0])) + " " + str(int(antenna.pos[1])) + "\n"

outFile.write(outString)
outFile.close()

executionTime = (time.time() - startTime)
print('Execution time in seconds: ' + str(executionTime))
