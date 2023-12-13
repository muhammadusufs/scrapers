import requests
from bs4 import BeautifulSoup


URL = "https://stadion.uz/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

data = []
games_list = []
results = soup.find(id="online_tablo").find("ul")

team = str(input("Jamoa nomini kiriting ==> "))

for li in results.findAll("li",recursive=False):
    league = li.find(id="online_tablo_title").find("b").text
    dumb_data = {'league': league}    
    games = []

    ul = li.find("ul")
    for ul_li in ul.findAll("li"):
        if ul_li.find("ul"):
            game_date = ul_li.find(id="online_tablo_day").text
            game_team1 = ul_li.find(id="online_tablo_team1").text
            result = ul_li.find(id="online_tablo_result").text
            game_team2 = ul_li.find(id="online_tablo_team2").text

            game = {
                "date":str(game_date).strip(),
                "team1":str(game_team1).strip(),
                "team2":str(game_team2).strip(),
                "result":str(result).strip(),
            }

            games.append(game)
            games_list.append(game)

    dumb_data.update({'games':games})

    data.append(dumb_data)

result = list(filter(lambda x: x['team1'] == team or x['team2'] == team, games_list))

if len(result) > 0:
    match_data = result[0]
    print(f"\nJamoa : {team}")
    print(f"Raqib jamoa : {match_data['team1'] if team == match_data['team2'] else match_data['team2']}")
    print(f"Hisob : {match_data['result'] if team == match_data['team1'] else str(match_data['result'])[::-1]}")
    print(f"Sana : {match_data['date']}")
else:
    print("Siz izlagan jamoa topilmadi :(")

print("\n===========")
print("|| Tablo ||")
print("===========")

for leage in data:
    print(f"\n{leage['league']}\n")
    for game in leage['games']:
        print(f"{game['date']} | {game['team1']} {game['result']} {game['team2']}")

    print("==========================================")
