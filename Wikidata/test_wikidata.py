import requests

r = requests.get('http://www.wikidata.org/entity/Q50745')
print(r.json())