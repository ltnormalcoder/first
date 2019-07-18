import requests
import json
url = r'http://23.228.74.242:5088'
params1 = {"q":"4354"}
response = requests.get(url=url,params=params1)
print(response.status_code)
data=json.loads(response.text)
print(data['useremail'])