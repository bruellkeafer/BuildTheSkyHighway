import random as rd
import numpy as np
import matplotlib.pyplot as plt


class Building:
    ReachableAntennas = []
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
            best_antenna = (0, antennas[rd.randint(0, len(antennas))])
        return best_antenna


class Antenna:
    def __init__(self, range_value, connection_speed):
        self.range = range_value
        self.connectionSpeedWeight = connection_speed
        self.pos = [None, None]
        self.assignedBuildings = []

    def assign_building(self, building):
        self.assignedBuildings.append(building)

    # def list_reachable_buildings(self, buildings_list):
    #     for a in buildings_list:
    #         if distance(self.X, self.Y, a.X, a.Y) <= a.Range:
    #             self.ReachableAntennas.append(a)


class Clustering:
    def __init__(self, antennas, buildings):
        self.antennas = antennas
        self.buildings = buildings
        self.NumberOfAntennas = len(antennas)
        for ant in self.antennas:
            ant.pos = [rd.randint(0, MapXLength), rd.randint(0, MapYLength)]

    def cluster_step(self):
        # build cluster groups
        for ind, building in enumerate(self.buildings):
            print("processing building " + str(ind) + '/' + str(len(self.buildings)))
            _, ant = building.find_best_antenna(self.antennas)
            ant.assign_building(building)

        for a in self.antennas:
            if len(a.assignedBuildings) != 0:
                a.pos = np.round(
                    np.average(list(map(lambda bld: bld.pos[0], a.assignedBuildings)))), np.round(
                    np.average(list(map(lambda bld: bld.pos[1], a.assignedBuildings))))


def distance(building, ant):
    return np.linalg.norm(np.array(building.pos) - np.array(ant.pos))


def total_score(buildings, reward):
    if any(hasattr(x, 'Score') for x in buildings):
        return 0
    return sum(list(map(lambda x: x.Score, buildings))) + reward


def get_score(building, ant):
    return (building.connectionSpeedWeight * ant.connectionSpeedWeight) - (
            building.latencyWeight * distance(ant, building))


def connect_building_to_antenna(building):
    building.connectedAntenna = max(list(map(lambda x: get_score(building, x), building.ReachableAntennas)))


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
# plot_map(Antennas,Buildings)

print("processing cluster step")
cl.cluster_step()
print("cluster step finished")

for c in cl.antennas:
    print(c.pos)
# plot_map(Antennas,Buildings)
outFile = open(
    "C:\\Users\\Tim Martins\\Desktop\\Projekte\\Programmieren\\ReplyChallenges\\TapTapTap\\BuildTheSkyHighway\\out.txt",
    "w")
outString = str(len(cl.antennas)) + "\n"
for index, antenna in enumerate(cl.antennas):
    outString += str(index) + " " + str(int(antenna.pos[0])) + " " + str(int(antenna.pos[1])) + "\n"

outFile.write(outString)
