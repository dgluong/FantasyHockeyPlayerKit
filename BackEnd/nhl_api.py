import requests
import json


class NhlScrape:
    def __init__(self):
        self.url = 'https://statsapi.web.nhl.com/'
        self.rosters = {}

    def get_all_teams(self):
        # The api contains every team in existence, therefore some do not
        # have roster, need to get every team and sort which one's have
        # active rosters, num_of_teams will eventually need to change
        num_of_teams = 55
        rosters = {}

        for i in range(1, num_of_teams + 1):
            endpoint = f"api/v1/teams/{i}/roster"
            data = requests.get(url=f"{self.url}{endpoint}")
            if data.ok:
                temp = {i: data.json()["roster"]}
                rosters.update(temp)

        print(json.dumps(rosters, indent=4, sort_keys=True))

    def get_team(self):
        # TEST FUNCTION
        roster = {}
        data = requests.get(url=f"{self.url}api/v1/teams/1/roster")
        roster.update({1: data.json()["roster"]})
        print(json.dumps(roster, indent=4, sort_keys=True))

        # modularize code here, needs to be own function
        for team in roster:
            for player in roster[team]:
                name = player["person"]["fullName"]
                position = player["position"]["code"]
                if not position == "G":
                    print(name)
                    print(position)
                    self.get_stats(player["person"]["link"])

    def get_stats(self, player_endpoint: str):
        endpoint = "/stats?stats=statsSingleSeason&season=20192020"
        data = requests.get(url=f"{self.url}{player_endpoint}{endpoint}")
        stats = data.json()['stats'][0]["splits"][0]['stat']
        print(stats)


if __name__ == '__main__':
    test = NhlScrape()
    # test.get_all_teams()
    test.get_team()
