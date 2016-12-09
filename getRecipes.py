import json
import SECRET
import requests

with open('data/ids.txt', 'rb') as f:
    recipeIds = f.read().decode("utf-8").splitlines()

# print(recipeIds)
for recipeId in recipeIds[100:]:
    url = "http://api.yummly.com/v1/api/recipe/%s?_app_id=%s&_app_key=%s" % (recipeId, SECRET.APP_ID, SECRET.APP_KEY)
    response = requests.get(url)
    outputFile = 'data/detail/' + recipeId + '.json'
    print(outputFile)
    with open(outputFile, 'w') as f:
        json.dump(response.text,  f)
