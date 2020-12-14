import requests
import json


class NhlScrape:
    def __init__(self):
        self.url = 'https://statsapi.web.nhl.com/'
        self.players = []
        # TODO add multiplier for each statistic for the player_score

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
        print(rosters)

        # TODO modularize code here, should be own function
        for team in rosters:
            for player in rosters[team]:
                name = player["person"]["fullName"]
                position = player["position"]["code"]
                player_endpoint = player["person"]["link"]
                if not position == "G":
                    stats = self.get_stats(player_endpoint)
                    temp = {"name": name}
                    temp.update(stats)
                    self.calculate_player_score(stats)
                    self.players.append(temp)
                    print(temp)

    def get_stats(self, player_endpoint: str):
        endpoint = "/stats?stats=statsSingleSeason&season=20192020"
        data = requests.get(url=f"{self.url}{player_endpoint}{endpoint}")
        splits = data.json()['stats'][0]['splits']
        if splits:
            stats = splits[0]['stat']
        else:
            stats = []
        return stats

    def calculate_player_score(self, stats):
        player_score = 'N/A'
        if stats:
            games = stats['games']
            for statistic in stats:
                if not ('time' in statistic.lower() or
                        'pct' in statistic.lower()):
                    print(statistic, stats[statistic])
        return player_score
    # stats to consider:
    # games --> have a minimum games played
    # assists
    # goals
    # pim
    # shots
    # hits
    # powerPlayGoals
    # powerPlayPoints
    # penaltyMinutes
    # gameWinningGoals
    # overTimeGoals --> may have a problem with this one for time
    # shortHandedGoals
    # blocked
    # plusMinus
    # points
    # shifts

if __name__ == '__main__':
    test = NhlScrape()
    test.get_all_teams()
    # test.get_team()
