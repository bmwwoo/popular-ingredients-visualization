import json
import csv
import matplotlib.pyplot as plt
import sys
import numpy as np
from matplotlib.mlab import PCA

sys.path.append("/usr/local/lib/python2.7/site-packages")

import seaborn as sns

csv.register_dialect(
    'mydialect',
    delimiter = ',',
    quotechar = '"',
    doublequote = True,
    skipinitialspace = True,
    lineterminator = '\r\n',
    quoting = csv.QUOTE_MINIMAL)

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

def getItemFrequency(recipeList, prop):
    # count the ingredients
    ingredientCount = {}
    for recipe in recipeList:
        for ingredient in recipe[prop]:
            if ingredient in ingredientCount:
                ingredientCount[ingredient] += 1
            else:
                ingredientCount[ingredient] = 1

    ingredientCountList = [ [k,v] for k, v in ingredientCount.items() ]
    ingredientCountList.sort(key=lambda x: x[1], reverse=True)

    return ingredientCountList

def aggregatePropertites(recipe):
    recipeObj = {}
    recipeObj["ingredients"] = recipe["ingredients"]
    recipeObj["rating"] = recipe["rating"]
    recipeObj["flavors"] = recipe["flavors"]
    recipeObj["recipeName"] = recipe["recipeName"]
    recipeObj["id"] = recipe["id"]
    if "cuisine" in recipe["attributes"]:
        recipeObj["ethnicity"] = recipe["attributes"]["cuisine"]
    else:
        recipeObj["ethnicity"] = ["Not found"]
    # print(recipe)
    return recipeObj

def getEthnicIngredientFrequency(allEthnicCountList, allRecipeList):
    allEthnicRecipes = {}
    allEthnicIngrFreq = {}
    for key in allEthnicCountList:
        ethnicity = key[0]
        allEthnicRecipes[ethnicity] = []
        allEthnicIngrFreq[ethnicity] = []

    for recipe in allRecipeList:
        for ethnicity in recipe["ethnicity"]:
            allEthnicRecipes[ethnicity].append(recipe)

    for ethnicity in allEthnicRecipes:
        allEthnicIngrFreq[ethnicity] = getItemFrequency(allEthnicRecipes[ethnicity], "ingredients")

    return allEthnicIngrFreq, allEthnicRecipes

def getRatingFrequency(recipeList):
    # # sort based on rating
    # recipeList.sort(key=lambda x: x["rating"], reverse=True)
    ratingIngrRecipes = {}
    ratingIngrFreq = {}
    for recipe in recipeList:
        if str(recipe["rating"]) not in ratingIngrRecipes:
            ratingIngrRecipes[str(recipe["rating"])] = []
        ratingIngrRecipes[str(recipe["rating"])].append(recipe)

    for rating, recipes in ratingIngrRecipes.items():
        ratingIngrFreq[rating] = getItemFrequency(recipes, "ingredients")

    return ratingIngrFreq, ratingIngrRecipes

# def sortByFlavors(recipeList):
    # for recipe in recipeList:
    #     if recipe['id'] is not None:
    #         print(recipe['id'] + '\n')
    # return recipeList.sort(key=lambda x: x["flavors"], reverse=True)

def doesAppearTogether(a, b, recipe):
    aHere = False
    bHere = False
    for ingredient in recipe["ingredients"]:
        if ingredient == a:
            aHere = True
        if ingredient == b:
            bHere = True

    return aHere and bHere

def getCorrelationMatrix(allRecipeList):
    #matrix = [[0] * 3] * 3
    matrix = []
    fmtMatrix = []
    for i in range(0,20):
        matrix.append([])
        fmtMatrix.append([])
        for j in range(0,20):
            matrix[i].append(0)
            fmtMatrix[i].append(0)

    for key1, value1 in mapping.items():
        for key2, value2 in mapping.items():
            for recipe in allRecipeList:
                if doesAppearTogether(key1, key2, recipe):
                    matrix[value1][value2] += 1

    sns.set(context="paper", font="monospace")

    # Load the datset of correlations between cortical brain networks
    df = sns.load_dataset("brain_networks", header=[0, 1, 2], index_col=0)

    for i, row in enumerate(matrix):
        for j, col in enumerate(row):
            if i == j:
                matrix[i][j] = 0
    for i, row in enumerate(matrix):
        rowSum = sum(row)
        for j, col in enumerate(row):
            fmtMatrix[i][j] = col / rowSum

    for i, row in enumerate(matrix):
        for j, col in enumerate(row):
            if matrix[i][j] != matrix[j][i]:
                print("DICKS")
    corrmat = fmtMatrix

    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(12, 9))

    # Draw the heatmap using seaborn
    sns.heatmap(corrmat, vmax=.15, square=True)

    sns.plt.show()

def performPCA(recipeList):
    N = 10
    xTrue = np.linspace(0, 10, N)
    yTrue = 3 * xTrue
    xData = xTrue + np.random.normal(0, 100, N)
    yData = yTrue + np.random.normal(0, 100, N)
    xData = np.reshape(xData, (N, 1))
    yData = np.reshape(yData, (N, 1))

    print(yData)
    data = np.hstack((xData, yData))
    print(data)

    soData = []
    swData = []
    biData = []
    piData = []
    saData = []
    meData = []
    for flavor in recipeList:
        if flavor["flavors"] is not None:
            soData.append(flavor["flavors"]["sour"])
            swData.append(flavor["flavors"]["sweet"])
            biData.append(flavor["flavors"]["bitter"])
            piData.append(flavor["flavors"]["piquant"])
            saData.append(flavor["flavors"]["salty"])
            meData.append(flavor["flavors"]["meaty"])

    N = np.asarray(soData).size

    soData = np.reshape(np.asarray(soData), (N, 1))
    swData = np.reshape(np.asarray(swData), (N, 1))
    biData = np.reshape(np.asarray(biData), (N, 1))
    piData = np.reshape(np.asarray(piData), (N, 1))
    saData = np.reshape(np.asarray(saData), (N, 1))
    meData = np.reshape(np.asarray(meData), (N, 1))

    data = np.hstack((soData, swData, biData, piData, saData, meData))

    results = PCA(data)

    print("Principle component axes in terms of the measurement axes scaled by the standard deviation: \n", results.Wt)
    print(results.fracs)
    # for i in data:
    #     print(i)
    # mu = data.mean(axis=0)
    # data = data - mu
    # # data = (data - mu)/data.std(axis=0)  # Uncommenting this reproduces mlab.PCA results
    # eigenvectors, eigenvalues, V = np.linalg.svd(data.T, full_matrices=False)
    # projected_data = np.dot(data, eigenvectors)
    # sigma = projected_data.std(axis=0).mean()

    # fig, ax = plt.subplots()
    # ax.scatter(soData, swData)
    # for axis in eigenvectors:
    #     start, end = mu[:2], mu[:2] + sigma * axis[:2]

    #     ax.annotate(
    #         '', xy=end, xycoords='data',
    #         xytext=start, textcoords='data',
    #         arrowprops=dict(facecolor='red', width=2.0))
    # ax.set_aspect('equal')
    # plt.show()


if __name__ == "__main__":
    # # Reading data back
    with open("foodNames.txt", "rb") as f:
        recipeNames = f.read().decode("utf-8").splitlines()


    allRecipeList = []
    for recipe in recipeNames:
        food_fmt = recipe.replace("+", "_")
        fileName = "data/" + food_fmt + ".json"
        with open(fileName, "r") as f:
            recepiesQuery = json.load(f)

        recipiesJson = json.loads(recepiesQuery)

        recipeList = []
        for recipe in recipiesJson["matches"]:
            recipeObj = aggregatePropertites(recipe)

            recipeList.append(recipeObj)
            allRecipeList.append(recipeObj)

        # sort the ingredients by most frequent
        ingredientCountList = getItemFrequency(recipeList, "ingredients")

        # print("Food: " + food_fmt)
        # print(ingredientCountList)
    #     # print("\n\n\n")
    performPCA(allRecipeList)

    # allIngredientCountList = getItemFrequency(allRecipeList, "ingredients")
    # allEthnicityCountList = getItemFrequency(allRecipeList, "ethnicity")
    # allEthnicIngrFrequency, allEthnicRecipes = getEthnicIngredientFrequency(allEthnicityCountList, allRecipeList)
    # allRatingIngrFrequency, allRatingIngrRecipes = getRatingFrequency(allRecipeList)
    # sortedFlavors = sortByFlavors(allRecipeList)

    # getCorrelationMatrix(allRecipeList)

    # print("Number of recipes: " + str(len(allRecipeList)))
    # print("Number of unique ingredients: " + str(len(allIngredientCountList)))
    # print("Most popular ingredients:")
    # for item in allIngredientCountList[:40]:
    #     print(str(item[0]) + ":\t" + str(item[1]))

    # # with open('mostPopular.csv', 'w') as mycsvfile:
    # #     thedatawriter = csv.writer(mycsvfile, dialect='mydialect')
    # #     for row in allIngredientCountList[:40]:
    # #         thedatawriter.writerow(row)

    # print("\n")

    # print("Most popular ethnicities:")
    # for item in allEthnicityCountList:
    #     print(str(item[0]) + ":\t" + str(item[1]))

    # print()
    # ethnicLength = {}
    # for ethnicity, val in allEthnicIngrFrequency.items():
    #     # print("Ethnicity: " + e)
    #     print("Number of ethnic " + ethnicity + " foods found: " + str(len(allEthnicRecipes[ethnicity])))
    #     ethnicLength[ethnicity] = len(allEthnicRecipes[ethnicity])

    #     print("Most popular ingredients:")
    #     for item in val[:10]:
    #         print(item[0] + ":\t" + str(item[1]))
    #     print()
    #     # with open("data/mostPopular/" + ethnicity + 'Popular.csv', 'w') as mycsvfile:
    #     #     thedatawriter = csv.writer(mycsvfile, dialect='mydialect')
    #     #     for row in val[:400]:
    #     #         thedatawriter.writerow(row)

    # # ethnicLengthList = []
    # # for key, value in ethnicLength.items():
    # #     temp = [key,value]
    # #     ethnicLengthList.append(temp)

    # # with open("ethnicCount.csv", "w") as mycsvfile:
    # #     for item in ethnicLengthList:
    # #         thedatawriter = csv.writer(mycsvfile, dialect='mydialect')
    # #         thedatawriter.writerow(item)

    # # for rating, val in allRatingIngrFrequency.items():
    # #     print("Number of recipes rated " + rating + ": " + str(len(allRatingIngrRecipes[rating])))
    # #     print("Most popular ingredients:")
    # #     for item in val[:10]:
    # #         print(str(item[0]) + ":\t" + str(item[1]))
    # #     print()

    # # totalLen = int(len(allIngredientCountList)/5)
    # # totalSum = 0
    # # firstSum = 0
    # # lastSum  = 0
    # # for i, item in enumerate(allIngredientCountList):
    # #     if i < totalLen:
    # #         firstSum += int(item[1])
    # #     else:
    # #         lastSum += int(item[1])
    # #     totalSum += int(item[1])
    # #     # print(i, item)

    # # print(firstSum)
    # # print(lastSum)
    # # print(totalSum)


