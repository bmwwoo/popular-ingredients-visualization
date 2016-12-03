import json
import SECRET
import requests

data = {
   'name' : 'ACME',
   'shares' : 100,
   'price' : 542.23
}

arr = [data, data]

# Writing JSON data
with open('dataDump.txt', 'w') as f:
    json.dump(arr,  f)

# # Reading data back
with open('dataDump.txt', 'r') as f:
     test = json.load(f)

param = "onion+soup"

url = "http://api.yummly.com/v1/api/recipes?_app_id=%s&_app_key=%s&q=%s" % (SECRET.APP_ID, SECRET.APP_KEY, param)

print(url)

response = requests.get(url)

print(response.text)

with open('recipes.json', 'w') as f:
    json.dump(response.text,  f)
