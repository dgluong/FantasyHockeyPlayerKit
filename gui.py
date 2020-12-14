import PySimpleGUI as sg
from FrontEnd.nhl_api import NhlScrape


# stats to consider:
# games
# assists
# goals
# pim
# shots
# hits
# powerPlayGoals
# powerPlayPoints
# penaltyMinutes
# gameWinningGoals
# overTimeGoals
# shortHandedGoals
# blocked
# plusMinus
# points
# shifts

stats = ['games', 'assists', 'goals', 'pim', 'shots', 'hits',
         'powerPlayGoals', 'powerPlayPoints',
         'gameWinningGoals', 'overTimeGoals', 'shortHandedGoals', 'blocked',
         'plusMinus', 'points', 'shifts']
layout = [[sg.Text("Stat Multipliers")]]

text_column = []
input_column = []
for stat in stats:
    text_column.append([sg.Text(stat)])
    input_column.append([sg.In(key=stat)])

output_file_row = [sg.Text("Output File Name:   "), sg.In(key="output")]
games_played_row = [sg.Text("Min Games Played: "), sg.In(key="games_played")]
per_game_row = [sg.Checkbox(key="per_game", text="Per Game Mode")]

layout.append([sg.Column(text_column), sg.Column(input_column)])
layout.append([sg.Text("")])
layout.append(games_played_row)
layout.append(output_file_row)
layout.append(per_game_row)
layout.append([sg.Button("Submit")])

window = sg.Window("Fantasy Hockey Player Tool", layout)

scraper = NhlScrape()

while True:
    event, values = window.read()
    try:
        scraper.set_scraper(**values)
        scraper.get_rosters()
    except TypeError as e:
        print(e)
    except ValueError as e:
        print("user value error")
    print(values)
    print(event)
    if event == sg.WIN_CLOSED:
        break

window.close()
