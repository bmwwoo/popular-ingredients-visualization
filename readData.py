import json

def getItemFrequency(recipeList, prop):
    # # sort based on rating
    # recipeList.sort(key=lambda x: x["rating"], reverse=True)

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
    recipeObj["recipeName"] = recipe["recipeName"]
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
    # print("\n\n\n")

allIngredientCountList = getItemFrequency(allRecipeList, "ingredients")
allEthnicityCountList = getItemFrequency(allRecipeList, "ethnicity")
allEthnicIngrFrequency, allEthnicRecipes = getEthnicIngredientFrequency(allEthnicityCountList, allRecipeList)

print("Number of recipes: " + str(len(allRecipeList)))
print("Number of unique ingredients: " + str(len(allIngredientCountList)))
print("Most popular ingredients:")
for item in allIngredientCountList[:40]:
    print(str(item[0]) + ":\t" + str(item[1]))

print("\n")

print("Most popular ethnicities:")
for item in allEthnicityCountList:
    print(str(item[0]) + ":\t" + str(item[1]))

for e, val in allEthnicIngrFrequency.items():
    # print("Ethnicity: " + e)
    print("Number of ethnic " + e + " foods found: " + str(len(allEthnicRecipes[e])))
    print("Most popular ingredients:")
    for item in val[:10]:
        print(item[0] + ":\t" + str(item[1]))
    print()

