from flask import Flask, render_template, json, request, jsonify
from datetime import datetime
import os.path

#Global var indicates the path to json file
jsonPath = "savedgames.txt"

#Class representation of a state of the game
class GameState:
    def __init__(self, first, second, third, fourth, fifth, sixth, seventh, eighth, ninth, date):
    	self.first = first
    	self.second = second
    	self.third = third
    	self.fourth = fourth
    	self.fifth = fifth
    	self.sixth = sixth
    	self.seventh = seventh
    	self.eighth = eighth
    	self.ninth = ninth
    	self.date = date
    	#TODO: turn into list

    def toJSON(self):
    	return {'p1':self.first,'p2':self.second, 'p3':self.third, 
        		'p4':self.fourth, 'p5':self.fifth, 'p6':self.sixth, 
        		'p7':self.seventh, 'p8':self.eighth, 'p9':self.ninth, 'date':self.date}
        		
app = Flask(__name__)

@app.route('/new_game/', methods=['GET', 'POST'])
def home():

	#Initial empty game
	initialGame = GameState('', '', '', '', '', '', '', '', '', '')
	
	#Case its a POST method, its loading a saved game or saving a new game
	if request.method == 'POST':
		#retrieves data in the form in the request from the selected saved game
		a = request.form['first']
		b = request.form['second']
		c = request.form['third']
		d = request.form['fourth']
		e = request.form['fifth']
		f = request.form['sixth']
		g = request.form['seventh']
		h = request.form['eighth']
		i = request.form['ninth']
		
		initialGame = GameState(first=a, second=b, third=c, 
								fourth=d, fifth=e, sixth=f, 
								seventh=g, eighth=h, ninth=i, date=str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

		#saves the game at the json file
		if request.form['flow'] == 'saving_game':
			
			jsonStr = json.dumps(initialGame.toJSON())
			
			f = open(jsonPath, "a")
			emptycontent = open(jsonPath, "r").read()
			if emptycontent: #in case the file is empty, wich means just created and there's no games saved
				f.write('/')
			f.write(jsonStr)
			f.close()

	return render_template('main.html', initialGame=initialGame)

@app.route("/just_saved_game", methods=['POST'])
def save():

	#retrieves data in the form in the request from the played game
	a = request.form['first']
	b = request.form['second']
	c = request.form['third']
	d = request.form['fourth']
	e = request.form['fifth']
	f = request.form['sixth']
	g = request.form['seventh']
	h = request.form['eighth']
	i = request.form['ninth']

	gametobesaved = GameState(first=a, second=b, third=c, 
							fourth=d, fifth=e, sixth=f, 
							seventh=g, eighth=h, ninth=i, date=str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

	#saves into json file
	jsonStr = json.dumps(gametobesaved.toJSON())
	
	f = open("savedgames.txt", "a")
	emptycontent = open("savedgames.txt", "r").read()
	if emptycontent:
		f.write('/')
	f.write(jsonStr)
	f.close()
	
	return render_template('main.html', initialGame=gametobesaved)

@app.route("/saved_games/")
def savedGames():

	savedGames = [] #saved games list

	#check if the file exists to avoid reading error
	if os.path.exists(jsonPath):
		#read the saved games in the json file
		s = open(jsonPath, "r")
		str = s.read()

		#case str is not empty to avoid function loads in empty json
		if str: 
			for obj in str.split('/'): #iterate over the saved games
				parsed_json = json.loads(obj)
				savedGame = GameState(parsed_json['p1'], parsed_json['p2'], parsed_json['p3'], 
									parsed_json['p4'], parsed_json['p5'], parsed_json['p6'], 
									parsed_json['p7'], parsed_json['p8'], parsed_json['p9'], parsed_json['date'])
				savedGames.append(savedGame)

			return render_template('saved_games.html', savedGames=savedGames)

	#in case it didnt return already, or the file doesnt exist or its empty. return message
	return render_template('saved_games.html', savedGames=savedGames, msg='Não há jogos salvos.')
