import PySimpleGUI as sg

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
         'powerPlayGoals', 'powerPlayPoints', 'penaltyMinutes',
         'gameWinningGoals', 'overTimeGoals', 'shortHandedGoals', 'blocked',
         'plusMinus', 'points', 'shifts']
categories = []

# for stat in stats:
#     categories.append(sg.Text(stat))
#     categories.append(sg.Input(key=stat))
categories.append(sg.Text(stats[0]))
categories.append(sg.Input(key=stats[0]))
categories.append(sg.Text(stats[1]))
categories.append(sg.Input(key=stats[1]))


layout = [categories, [sg.Button("test")]]

window = sg.Window("Demo", layout)

while True:
    event, values = window.read()
    print(values)
    print(event)
    if event == sg.WIN_CLOSED:
        break

window.close()
