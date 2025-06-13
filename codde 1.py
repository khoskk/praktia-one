import requests
import json

service_key = "2e6dae412e6dae412e6dae41cf2d47c51222e6d2e6dae4149db719968f1915c5562d0eb"
VK_CONFIG = {
    "domain": "https://api.vk.com/method",
    "access_token": service_key,
    "version": "5.199",

}


wall_domain = "itmostudents"
count = 50
offset = 0

posts = []
for i in range(5):
    query = f"{VK_CONFIG['domain']}/wall.get?access_token={VK_CONFIG['access_token']}&domain={wall_domain}&v={VK_CONFIG['version']}&count={count}&offset={offset}"
    response = requests.get(query)

    posts += [res["text"] for res in response.json()["response"]["items"]]
    print(offset)
    offset += 50



to_save = {n: post for n, post in enumerate(posts)}

with open("vk_data.json", "w", encoding="utf-8") as f:
  json.dump(to_save, f, ensure_ascii=False, indent=4)


with open("vk_data.json", "r", encoding="utf-8") as f:
  from_file = json.load(f)
