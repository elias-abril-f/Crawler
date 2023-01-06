import json

regions={}
with open('./main/static/main/postcodes.json', 'r') as f:
    regions = json.load(f)
    
print(regions["N1"])