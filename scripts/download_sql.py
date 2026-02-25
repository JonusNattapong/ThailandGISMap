import requests
import os

url = "https://raw.githubusercontent.com/JonusNattapong/ThailandLocation77DatabaseSQLServer/main/Dataset/thailand_sqlserver.sql"
target = "data/thailand_sqlserver.sql"

print(f"Downloading {url}...")
response = requests.get(url)
if response.status_code == 200:
    with open(target, 'wb') as f:
        f.write(response.content)
    print(f"Downloaded to {target}")
else:
    print(f"Failed to download. Status code: {response.status_code}")
