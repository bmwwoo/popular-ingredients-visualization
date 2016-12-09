import matplotlib.pyplot as plt
import csv
import numpy as np
import scipy.stats as spstats

ethnicities = ["Not found", "Kid-Friendly", "Asian", "Indian", "Barbecue", "English", "Chinese", "Italian", "French", "Mexican", "Irish", "Southern & Soul Food", "German", "Greek", "American", "Cajun & Creole", "Thai", "Mediterranean", "Southwestern", "Japanese", "Vietnamese", "Moroccan", "Filipino", "Korean", "Jamaican", "Swedish", "Spanish", "Portuguese", "Turkish", "Cuban", "Hawaiian", "Hungarian", "Russian", "Brazilian"]

mapping = { "salt" : 0,
            "butter" : 1,
            "sugar" : 2,
            "water" : 3,
            "eggs" : 4,
            "olive oil" : 5,
            "onions" : 6,
            "garlic" : 7,
            "pepper" : 8,
            "milk" : 9,
            "unsalted butter" : 10,
            "all-purpose flour" : 11,
            "flour" : 12,
            "kosher salt" : 13,
            "baking powder" : 14,
            "garlic cloves" : 15,
            "vanilla extract" : 16,
            "large eggs" : 17,
            "lemon juice" : 18,
            "vegetable oil" : 19
            }

csv.register_dialect(
    'mydialect',
    delimiter = ',',
    quotechar = '"',
    doublequote = True,
    skipinitialspace = True,
    lineterminator = '\r\n',
    quoting = csv.QUOTE_MINIMAL
    )

def findChiSquareStat(mostPopularAllValues, ethnicValues):
    diffArr = []
    for overall, ethnic in zip(mostPopularAllValues, ethnicValues):
        diffArr.append((ethnic - overall) ** 2 / overall)
    return sum(diffArr)

def findChiSquareProb(data):
    return spstats.chi2.cdf(data, 19)

    # print(ChiSquareProbability)

mostPopularAllKeys = []
mostPopularAllValues = []
with open('mostPopular.csv', 'r', encoding="ascii") as mycsvfile:
    data = csv.reader(mycsvfile, dialect='mydialect')
    for row in data:
        mostPopularAllKeys.append(row[0])
        mostPopularAllValues.append(int(row[1]) / 11739)

allEthnicLen = {}
with open("ethnicCount.csv", "r") as f:
    data = csv.reader(f, dialect="mydialect")
    for row in data:
        allEthnicLen[row[0]] = float(row[1])

allEthnicFreq = {}
for ethnic in ethnicities:
    with open("data/mostPopular/" + ethnic + "Popular.csv", 'r') as mycsvfile:
        data = csv.reader(mycsvfile, dialect='mydialect')
        ethnicFreq = {}
        for row in data:
            ethnicFreq[row[0]] = float(row[1]) / allEthnicLen[ethnic]
        allEthnicFreq[ethnic] = ethnicFreq

chiSquareList = []
for ethnic, eList in allEthnicFreq.items():
    buckets = [0] * 20
    for key, val in eList.items():
        if key in mapping:
            buckets[mapping[key]] = val
    chiSquareStat = findChiSquareStat(mostPopularAllValues, buckets)
    chiSquareList.append(chiSquareStat)
    # print(chiSquareStat)

for chiSquareStat in chiSquareList:
    ChiSquareProbability = findChiSquareProb(chiSquareStat)
    print(ChiSquareProbability)

# plt.xticks(rotation=90)
# plt.bar(range(len(mostPopularAllValues)), mostPopularAllValues, align='center')
# plt.xticks(range(len(mostPopularAllValues)), mostPopularAllKeys, size='small')
# plt.show()



