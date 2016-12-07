import json
import SECRET
import requests

with open('foodNames.txt', 'rb') as f:
    recipeNames = f.read().decode("utf-8").splitlines()

print(recipeNames)

for name in recipeNames:
    url = "http://api.yummly.com/v1/api/recipes?_app_id=%s&_app_key=%s&q=%s" % (SECRET.APP_ID, SECRET.APP_KEY, name)
    print(url)
    response = requests.get(url)
    food_fmt = name.replace("+", "_")
    outputFile = 'data/' + food_fmt + '.json'
    print(outputFile)
    with open(outputFile, 'w') as f:
        json.dump(response.text,  f)
