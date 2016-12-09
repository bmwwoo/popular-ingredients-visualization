import json
import re

def sanitizeIngredients(ingredientList):
    ingrList = []
    for ingredient in ingredientList:
        number = re.search(r'\d+', ingredient)
        if number is not None:
            ingrList.append(number.group(0))

    return ingrList


def aggregateDetails(recipe):
    recipeObj = {}
    recipeObj["ingredientLines"] = sanitizeIngredients(recipe["ingredientLines"])

    recipeObj["rating"] = recipe["rating"]
    recipeObj["flavors"] = recipe["flavors"]
    recipeObj["name"] = recipe["name"]
    recipeObj["numberOfServings"] = recipe["numberOfServings"]
    recipeObj["totalTimeInSeconds"] = recipe["totalTimeInSeconds"]

    if "cuisine" in recipe["attributes"]:
        recipeObj["ethnicity"] = recipe["attributes"]["cuisine"]
    else:
        recipeObj["ethnicity"] = ["Not found"]

    return recipeObj

if __name__ == "__main__":
    # # Reading data back
    with open("foodNames.txt", "rb") as f:
        recipeNames = f.read().decode("utf-8").splitlines()
    with open("data/ids.txt", "rb") as f:
        recipeIds = f.read().decode("utf-8").splitlines()

    allRecipeObj = []
    for recipe in recipeIds[:1000]:
        fileName = "data/detail/" + recipe + ".json"
        with open(fileName, "r") as f:
            recipeDetail = json.load(f)

        recipeDetailJson = json.loads(recipeDetail)
        recipeObj = aggregateDetails(recipeDetailJson)
        allRecipeObj.append(recipeObj)

    for recipe in allRecipeObj:
        print(recipe["rating"])
        # for ingredient in recipe["ingredientLines"]:
        #     print(ingredient)
