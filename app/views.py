from flask import render_template
from flask import jsonify
from flask import request
from pprint import pprint
from app import app

#update SQL
def update(date,time,description):
	app.logger.debug('updating the SQL!')
	record = mongo.db.records
	record.insert({'date': date, 'time': time, 'description': description})
	return;
	
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
	#pprint (vars(request))
	#app.logger.debug(request.args.get('dates', ''))
	if request.args.get('date', '') and request.args.get('time', '') and request.args.get('description', ''):
		#add to sql table
		update( request.args.get('date',''), request.args.get('time',''), request.args.get('description','') )
	return render_template('index.html')

@app.route('/api', methods=['GET'])
def api():
	headers = ["Date","Time","Description"]
	#if there is a search parameter query the DB for search otherwise query for all records here
	#sample data = [
        #{"date": "may 2", "time":"11:00am","description": "blah"},
        #{"date": "june 3", "time":"12:00pm","description": "blah blah"}
        #]
	record = mongo.db.records
        output = []
	if request.args.get('search', ''):
		date = record.find_one({ 'date': request.args.get('search', '')} ) #search for matching date
		time = record.find_one({ 'time': request.args.get('search', '')} ) #search for matching time
		desc = record.find_one({ 'description': request.args.get('description', '')} ) #search for matching description
		if date or time or desc:
			output = [{'date': record['date'], 'time': record['time'], 'description': record['description']}]
	else:
		for i in record.find():
			output.append({'date': record['date'], 'time': record['time'], 'description': record['description']})
	return jsonify(headers=headers,data=output)
