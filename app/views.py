from flask import render_template
from flask import jsonify
from flask import request
from pprint import pprint
from app import app
from app import mongo

def update(date,time,description):
	record = mongo.db.records.insert({'date': date, 'time': time, 'description': description})
	app.logger.debug('updating the SQL!')
	return;
	
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
	if request.args.get('date', '') and request.args.get('time', '') and request.args.get('description', ''):
		update( request.args.get('date',''), request.args.get('time',''), request.args.get('description','') )
	app.logger.debug('displaying the index')
	return render_template('index.html')

@app.route('/api', methods=['GET'])
def api():
	headers = ["Date","Time","Description"]
	record = mongo.db.records
        results = []
	output = []
	if request.args.get('search', ''):
		if record.find_one( { 'date': request.args.get('search', '')} ):
			results = record.find({'date': request.args.get('search', '')})
		elif record.find_one({ 'time': request.args.get('search', '')} ):
			results = record.find({'time': request.args.get('search', '')})
		elif record.find_one({ 'description': request.args.get('search', '')} ):
			results = record.find({'description': request.args.get('search', '')})
	else:
		results = record.find()
	for r in results:
                        output.append({'date': r['date'], 'time': r['time'], 'description': r['description']})
	app.logger.debug("sending the json!")
	return jsonify(headers=headers,data=output)
