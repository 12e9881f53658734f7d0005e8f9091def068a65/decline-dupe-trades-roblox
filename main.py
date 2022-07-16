import requests
from time import sleep

cookie = ""

# TODO
# Add error handling for when xcsrf expires
# am to lazy to do right now
# fix stuff i think probably 

USERIDS = {}

def gettoken(cookies):
    r = requests.post("https://auth.roblox.com/v1/logout", cookies=cookies)
    if r.status_code == 200 or r.status_code == 403:
        return r.headers["x-csrf-token"]
    else:
        print("Invalid Cookie.")


cookies = {
    ".ROBLOSECURITY": cookie
}
headers = {
    "x-csrf-token": gettoken(cookies),
}

url = "https://trades.roblox.com/v1/trades/inbound"

nextcursor = ""

while True:
    print(nextcursor)
    if nextcursor != "":
        trades = requests.get(f"https://trades.roblox.com/v1/trades/inbound?cursor={nextcursor}&limit=100&sortOrder=Desc", cookies=cookies, headers=headers)
    else:
        trades = requests.get("https://trades.roblox.com/v1/trades/inbound?limit=100&sortOrder=Desc", cookies=cookies, headers=headers)

    trades = trades.json()
    print(trades)
    for trade in trades["data"]:
        str1 = str(trade["user"]["id"])
        str2 = str(trade["id"])

        try:
            USERIDS[str1].append(str2)
        except KeyError:
            USERIDS.update({str1:[str2]})

    if trades["nextPageCursor"] == None:
        break
    
    nextcursor = trades["nextPageCursor"]
    sleep(1)

for userid in USERIDS:
    if len(USERIDS[userid]) >= 2:
        for tradeid in USERIDS[userid]:
            # g = requests.options(f"https://trades.roblox.com/v1/trades/{tradeid}/decline")
            # print(g)
            q = requests.post(f"https://trades.roblox.com/v1/trades/{tradeid}/decline", cookies=cookies, headers=headers)
            print(q.json())
        sleep(0.1)
