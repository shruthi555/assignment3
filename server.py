import os
from flask import Flask,render_template, url_for, flash, redirect, request
from tinydb import TinyDB, Query


PEOPLE_FOLDER = os.path.join('static', 'people_photo')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
open('names.json', 'w').close()

db = TinyDB('names.json')

filepath = 'names.csv'
with open(filepath) as fp:
	line=fp.readline().rstrip('\n')
	attributes = line.split(',')
	line = fp.readline().rstrip('\n')
	while line:
		values = line.split(',')
		item = {}
		for i in range(len(attributes)):
			item[attributes[i]] = values[i]
		db.insert(item)

		line = fp.readline().rstrip('\n')


@app.route('/')
def index():
	results = db.all()
	return render_template('index.html', image_folder=PEOPLE_FOLDER, results = results)

@app.route('/addnums', methods=['POST'])
def addnums():
	first = request.form['first']
	second = request.form['second']
	total = int(first)+int(second)
	return render_template('add.html', first=first, second=second, total=total)

@app.route('/stateall', methods=['POST'])
def stateall():
	state = request.form['state']
	Todo = Query()
	results = db.search(Todo.State == state)
	return render_template('state.html', results=results, image_folder=PEOPLE_FOLDER)

@app.route('/updatedata', methods=['POST'])
def updatedata():
	name = request.form['name']
	state = request.form['state']
	caption = request.form['caption']
	Todo = Query()
	results1 = db.search(Todo.Name == name)
	outputsize = len(results1)
	db.update({"State": state, "Caption" : caption}, Todo.Name.search(name))
	results2 = db.search(Todo.Name == name)
	return render_template('updateddata.html', message="successfully updated your state and caption", outputsize = outputsize, results1=results1, results2=results2)


port = int(os.getenv('PORT', '5000'))

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=port)