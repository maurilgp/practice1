import requests, json
from pprint import pprint as pp

def main():
    key = "6bec40cf957de430a6f1f2baa056b99a4fac9ea0"
    url = "https://dashboard.meraki.com/api/v0/organizations/681155/admins?X-Cisco-Meraki-API-Key="+key
    headers = { "X-Cisco-Meraki-API-Key" : "6bec40cf957de430a6f1f2baa056b99a4fac9ea0"}
    r = requests.get(url=url,headers=headers)
    print("Attempting opening URL: "+url)
    print("Status Code: "+str(r.status_code))
    print("Encoding: "+str(r.encoding))
    print("Links: "+str(r.links))
    print("--------------------------Content------------------------------")
    print(r.text)
    print("---------------------------------------------------------------")
    print()
    json_list = r.json()
    print(type(json_list))
    print("----------------------------JSON-------------------------------")
    pp(json_list)
    print("---------------------------------------------------------------")


if __name__ == "__main__":
    main()