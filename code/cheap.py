import random

file = open(
    "C:\\Users\\Tim Martins\\Desktop\\Projekte\\Programmieren\\ReplyChallenges\\TapTapTap\\BuildTheSkyHighway"
    "\\data_scenarios_f_tokyo(1).in",
    "r")

string = file.read()
inputs = string.split("\n")
# Line 1 - Map Read
MapScale = inputs[0].split(" ")
MapXLength = int(MapScale[0])
MapYLength = int(MapScale[1])
# Line 2 - Resources Read
ResourceInformation = inputs[1].split(" ")
AntennasCount = int(ResourceInformation[1])


def besetzt(x, y):
    for bla in outArr:
        if bla[0] == x and bla[1] == y:
            return True
    return False


outFile = open("out_f.txt", "w")

outArr = []
for i in range(AntennasCount):
    x = random.randint(0, MapXLength - 1)
    y = random.randint(0, MapYLength - 1)
    while besetzt(x, y):
        x = random.randint(0, MapXLength - 1)
        y = random.randint(0, MapYLength - 1)
    outArr.append((x,y))

outString = str(AntennasCount)
for ind, res in enumerate(outArr):
    outString += "\n" + str(ind) + " " + str(res[0]) + " " + str(res[1])

outFile.write(outString)
outFile.close()

print("moin")
