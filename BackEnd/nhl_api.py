import requests
import json


class NhlScrape:
    def __init__(self):
        self.url = 'https://statsapi.web.nhl.com/api/v1/'

    def get_all_teams(self):
        # The api contains every team in existence, therefore some do not
        # have roster, need to get every team and sort which one's have
        # active rosters
        num_of_teams = 55
        rosters = {}

        for i in range(1, num_of_teams + 1):
            endpoint = f"teams/{i}/roster"
            data = requests.get(url=f"{self.url}{endpoint}")
            if data.ok:
                temp = {i: data.json()["roster"]}
                rosters.update(temp)

        print(json.dumps(rosters, indent=4, sort_keys=True))


if __name__ == '__main__':
    test = NhlScrape()
    test.get_all_teams()
