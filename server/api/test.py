
import flask
from app import application

## Test Functions

@application.route('/api/test/public', methods = ['POST'])
@application.public
def public(identity):
	return flask.jsonify({ 'identity' : identity , 'api' : 'test' , 'action' : 'public' })

@application.route('/api/test/private', methods = ['POST'])
@application.authenticated
def private(identity):
	data = 'some private data'
	return flask.jsonify({ 'identity' : identity , 'api' : 'test' , 'action' : 'private' })

@application.route('/api/test/admin', methods = ['POST'])
@application.admin
def admin(identity):
	data = 'some admin data'
	return flask.jsonify({ 'identity' : identity , 'api' : 'test' , 'action' : 'admin' })

