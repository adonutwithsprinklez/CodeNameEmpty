from gameClass import Game
from jsonDecoder import loadJson, saveJson


GAME_VERSION = 0.1
MIN_DATA_PACK_VERSION = 0.1
MIN_SAVE_VERSION = 0.1


# Starts the gameloop
def startGame(game):
	game.loadPlayer()
	while True:
		game.displayCurrentArea()
		game.reactCurrentArea()
		if game.player.quit:
			return None
		game.chooseNewArea()
		if game.player.quit:
			return None
		if game.player.hp <= 0:
			# TODO have actual end of game code due to player death
			return False

def openSettings(game, settingsFile):
	game.openOptionsWindow()
	saveJson(settingsFile, game.settings)
	game.initialLoad(RES_FOLDER, SETTINGS)

def openDataPacks(game, settingsFile):
	game.openDataPacks()
	saveJson(settingsFile, game.settings)
	game.initialLoad(RES_FOLDER, SETTINGS)


# This code runs with main.py is opened
if __name__ == "__main__":
	# Loads some resource stuff
	RES_FOLDER = "res/"
	SETTINGS_FILE = RES_FOLDER + "settings.json"
	SETTINGS = loadJson("{}".format(SETTINGS_FILE))

	# Inital game / menu loading
	game = Game()
	game.initialLoad(RES_FOLDER, SETTINGS)

	appRunning = True
	while appRunning and game.disp.window_is_open:
		game.displayMainMenu()
		try:
			# cmd = int(input())
			cmd = game.disp.get_input(True)
			print(cmd)
		except ValueError:
			cmd = -1
		except:
			cmd = -1
			appRunning = False
		
		if cmd == 1:
			# Actually start the game
			startGame(game)
		elif cmd == 2:
			# Displays the settings menu
			openSettings(game, SETTINGS_FILE)
		elif cmd == 3:
			# Displays the data pack menu
			openDataPacks(game, SETTINGS_FILE)
		elif cmd == 0:
			# Exit the game
			appRunning = False
		else:
			pass #TODO finish incorrect command message
	game.shutdown_game()