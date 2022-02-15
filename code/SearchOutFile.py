
file = open(
    "..\\out.txt",
    "r")

string = file.read()
inputs = string.split("\n")
arr = []
for ind,inp in enumerate(inputs[1:]):
    values = inp.split(" ")
    i = values[0]
    x = values[1]
    y = values[2]
    arr.append((i,x,y))

for x in arr:
    for y in arr:
        if(x[0] != y[0] and x[1] == y[1] and x[2] == y[2]):
            print(x[0] + ':' + y[0] + "\t" + x[1] + '/' + x[2])
print("moin")
