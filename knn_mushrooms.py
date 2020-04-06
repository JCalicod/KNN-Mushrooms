import sys
import csv
import math

## Global variables
filename = sys.argv[1]
type = sys.argv[2]
selected = int(sys.argv[3])

def showKNeighbours(neighbours, data, individual, k):
    nb_selected = 0
    for i in range(len(neighbours)):
        selected_value = data[neighbours[i][1]][selected]
        if (selected_value == individual[0]):
            nb_selected = nb_selected + 1
        print("Voisin N° " + str(neighbours[i][1] - 1) + " distance : " + str(neighbours[i][0]) + " classe: " + str(selected_value))
    print("total : " + str(individual[0]) + ": " + str(nb_selected) + "/" + str(k))
    
def findKNN(data, individual, k):
    neighbours = []
    for i in range(k):
        neighbour = find1NN(data, individual)
        neighbours.append((neighbour[0], neighbour[1]))
        data[neighbour[1]].append('done')
    return neighbours


def find1NN(data, individual):
    final_diff = math.sqrt(len(data[1]))
    pos = -1
    for i in range(len(data)):
        if (i != 0):
            diff = getEuclideanDistance(data, individual, i)
            if (diff != -1 and diff < final_diff):
                final_diff = diff
                pos = i
    return (final_diff, pos)

def getEuclideanDistance(data, individual, data_index):
    if (len(individual) == len(data[data_index])):
        diff = 0
        for i in range(len(data[data_index])):
            if (data[data_index][i] != individual[i] and i != selected) or (i == selected):
                diff = diff + 1
        return math.sqrt(diff)
    return math.sqrt(len(individual))

def getSpecificData(data, field):
    nb = 0
    for i in range(len(data)):
        if (data[i][0] == field):
            nb = nb + 1
    return nb

def showStats(data):
    print(str(len(data) - 1) + " individus de type " + type)
    print(str(len(data[0])) + " attributs")
    print("prediction : " + str(data[0][0]) + "(p: " + str(getSpecificData(data, 'p')) + ", e: " + str(getSpecificData(data, 'e')) + ")")

def getFileData(filename):
    data = []
    file = open(filename, "r")

    try:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    finally:
        file.close()

    return data

def getList(row):
    return row.split(",")

def getUserInput(asking):
    print(asking)
    return input()

data = getFileData(filename)
print("Chargement du fichier " + filename)
showStats(data)
individual = getList(getUserInput("Entrez un individu à évaluer (valeurs séparées par des ',', comme dans le fichier chargé)"))
print("1NN pour cet individu : " + str(find1NN(data, individual)[0]))
k = int(getUserInput("Veuillez choisir K :"))
neighbours = findKNN(data, individual, k)
showKNeighbours(neighbours, data, individual, k)
