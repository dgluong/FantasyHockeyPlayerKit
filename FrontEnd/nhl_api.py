from csv import DictWriter
import requests
import json


# stats to consider:
# games --> have a minimum games played
# assists
# goals
# pim
# shots
# hits
# powerPlayGoals
# powerPlayPoints
# gameWinningGoals
# overTimeGoals --> may have a problem with this one for time
# shortHandedGoals
# blocked
# plusMinus
# points
# shifts

class NhlScrape:
    def __init__(self, **kwargs):
        self.url = 'https://statsapi.web.nhl.com/'
        self.players = []
        self.multipliers = None
        self.games_played = None
        self.output_file = None
        self.per_game = None

    def set_scraper(self, **kwargs):
        self.multipliers = kwargs
        self.games_played = int(kwargs['games_played'])
        self.output_file = kwargs['output']
        self.per_game = int(kwargs['per_game'])
        del self.multipliers['games_played']
        del self.multipliers['output']
        del self.multipliers['per_game']

    def get_rosters(self):
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

        # TODO modularize code here, should be own function
        for team in rosters:
            for player in rosters[team]:
                name = player["person"]["fullName"]
                position = player["position"]["code"]
                player_endpoint = player["person"]["link"]
                if not position == "G":
                    stats = self.get_stats(player_endpoint)
                    player_score = self.calculate_player_score(stats)
                    temp = {"name": name, "position": position}
                    temp.update({"player_score": player_score})
                    temp.update(stats)
                    self.players.append(temp)
        self.write_excel()

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
        player_score = 0
        if stats:
            games = stats['games']
            if games > self.games_played:
                for value in self.multipliers:
                    if self.per_game:
                        stat = float(stats[value]) / games
                    else:
                        stat = float(stats[value])
                    multiplier = float(self.multipliers[value])
                    player_score += self.multiply_stat(stat, multiplier)
        print(f"player score: {player_score}")
        return player_score

    def multiply_stat(self, stat, multiplier):
        player_score = stat * multiplier
        return player_score

    def write_excel(self):
        keys = [key for key in self.players[0].keys()]
        print(keys)

        with open(f'{self.output_file}.csv', 'w') as outfile:
            writer = DictWriter(outfile, restval="-", fieldnames=keys)
            writer.writeheader()
            writer.writerows(self.players)


if __name__ == '__main__':
    """Test input"""
    settings = {
        'games': '1',
        'assists': '1',
        'goals': '1',
        'pim': '.5',
        'shots': '.3',
        'hits': '.2',
        'powerPlayGoals': '0',
        'powerPlayPoints': '1',
        'gameWinningGoals': '0',
        'overTimeGoals': '0',
        'shortHandedGoals': '0',
        'blocked': '.5',
        'plusMinus': '1',
        'points': '1',
        'shifts': '0',
        'games_played': '40',
        'output': 'test',
        'per_game': True
    }

    test = NhlScrape()
    test.set_scraper(**settings)
    test.get_rosters()
    test.write_excel()
