# Rushy Panchal
# generate-history.py

import mongokit
import models
import json
import csv

def main():
	'''Main process'''
	conn = mongokit.Connection()
	conn.register(models.Game)
	models.register(conn)

	all_games = conn.Game.find().sort("timestamp", 1)
	num_games = all_games.count()

	games = []
	seemedHuman = 0

	for index, game in enumerate(all_games, 1):
		seemedHuman += int(game.seemedHuman)
		gameData = {
			"timestamp": str(game.timestamp),
			"human": game.seemedHuman,
			"gameNumber": index,
			"percentageHuman": float(seemedHuman) / index
			}
		games.append(gameData)

	with open("history.json", "w") as history:
		json.dump(games, history)

	with open("history.csv", "w") as history:
		writer = csv.writer(history)
		writer.writerow(["gameNumber", "timestamp", "human", "percentageHuman"])

		for game in games:
			writer.writerow([game["gameNumber"], game["timestamp"], game["human"], game["percentageHuman"]])

if __name__ == '__main__':
	main()
