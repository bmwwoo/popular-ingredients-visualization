import json
import SECRET
import requests

param = "onion+soup"

url = "http://api.yummly.com/v1/api/recipes?_app_id=%s&_app_key=%s&q=%s" % (SECRET.APP_ID, SECRET.APP_KEY, param)

print(url)

response = requests.get(url)

print(response.text)

with open('recipes.json', 'w') as f:
    json.dump(response.text,  f)
