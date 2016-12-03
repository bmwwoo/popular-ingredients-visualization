import json

# # Reading data back
with open('onionSoupSample.json', 'r') as f:
     recepiesQuery = json.load(f)

recipiesJson = json.loads(recepiesQuery)

recipeList = []
for recipe in recipiesJson["matches"]:
    recipeObj = {}
    recipeObj["ingredients"] = recipe["ingredients"]
    recipeObj["rating"] = recipe["rating"]
    recipeObj["recipeName"] = recipe["recipeName"]
    recipeList.append(recipeObj)

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
print(ingredientCountList)
