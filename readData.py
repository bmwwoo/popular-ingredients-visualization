import json

# # Reading data back
with open('foodNames.txt', 'rb') as f:
    recipeNames = f.read().decode("utf-8").splitlines()

allRecipeList = []
numRecipes = 0
for recipe in recipeNames:
    food_fmt = recipe.replace("+", "_")
    fileName = 'data/' + food_fmt + '.json'
    with open(fileName, 'r') as f:
        recepiesQuery = json.load(f)

    recipiesJson = json.loads(recepiesQuery)

    recipeList = []
    for recipe in recipiesJson["matches"]:
        recipeObj = {}
        recipeObj["ingredients"] = recipe["ingredients"]
        recipeObj["rating"] = recipe["rating"]
        recipeObj["recipeName"] = recipe["recipeName"]
        recipeList.append(recipeObj)
        allRecipeList.append(recipeObj)
        numRecipes += 1

    # sort based on rating
    recipeList.sort(key=lambda x: x["rating"], reverse=True)

    # count the ingredients
    ingredientCount = {}
    for recipe in recipeList:
        for ingredient in recipe["ingredients"]:
            if ingredient in ingredientCount:
                ingredientCount[ingredient] += 1
            else:
                ingredientCount[ingredient] = 1

    ingredientCountList = [ [k,v] for k, v in ingredientCount.items() ]
    ingredientCountList.sort(key=lambda x: x[1], reverse=True)
    print("Food: " + food_fmt)
    print(ingredientCountList)
    print('\n\n\n')


# sort based on rating
allRecipeList.sort(key=lambda x: x["rating"], reverse=True)

# count the ingredients
ingredientCount = {}
for recipe in allRecipeList:
    for ingredient in recipe["ingredients"]:
        if ingredient in ingredientCount:
            ingredientCount[ingredient] += 1
        else:
            ingredientCount[ingredient] = 1

ingredientCountList = [ [k,v] for k, v in ingredientCount.items() ]
ingredientCountList.sort(key=lambda x: x[1], reverse=True)
print("Number of recipes: " + str(numRecipes))
print(ingredientCountList)
